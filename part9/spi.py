
(INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN, 
BEGIN, END, SEMI, DOT, EOF) = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'ID', 'ASSIGN',
    'BEGIN', 'END', 'SEMI', 'DOT', 'EOF'
)

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        # keyword dictionary
        self.keywords = {
            'BEGIN': Token(BEGIN, 'BEGIN'),
            'END': Token(END, 'END')
        }
    
    def error(self):
        raise Exception('Unknown character ' + self.current_char)

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]
    
    def skip_whitespace(self):
        while self.current_char != None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        result = ''
        while self.current_char != None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def _id(self):
        result = ''
        while self.current_char != None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        token = self.keywords.get(result, Token(ID, result))
        return token
    
    def get_next_token(self):
        while self.current_char != None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.current_char.isalpha():
                return self._id()
            
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, "(")
            
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ")")
            
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, "+")
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, "-")
            
            if self.current_char == '*':
                self.advance()
                return Token(MUL, "*")
            
            if self.current_char == '/':
                self.advance()
                return Token(DIV, "/")
            
            if self.current_char == '.':
                self.advance()
                return Token(DOT, ".")
            
            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ";")
            
            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ":=")
            
            self.error()

        return Token(EOF, None)
    
class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Compound(AST):
    """Represents a 'BEGIN ... END' block"""
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left # variable name
        self.token = self.op = op # what is this for?
        self.right = right # expression

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()
    
    def error(self):
        raise Exception('Syntax Error')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        """
            program : compound_statement DOT
        """
        node = self.compound_statement()
        self.eat(DOT)
        return node
    
    def compound_statement(self):
        """
            compound_statement : BEGIN statement_list END
        """
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        
        # fill the statements
        root = Compound()
        for node in nodes:
            root.children.append(node)
        
        return root

    def statement_list(self):
        """ 
        statement_list : statement (SEMI statement)*
        """
        node = self.statement()
        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        # why did you put these lines here?
        if self.current_token.type == ID:
            self.error()

        return results
    
    def statement(self):
        """
        statement : compound_statement 
                  | assignment_statement 
                  | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN Expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node
    
    def variable(self):
        """ 
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node
    
    def empty(self):
        """ 
        empty : None
        """
        return NoOp()

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(node, token, self.term())

        return node

    def term(self):
        """
        term : factor ((MUL | DIV) factor)*
        """
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(node, token, self.term())

        return node

    def factor(self):
        """
         factor : PLUS     factor
                | MINUS    factor
                | INTEGER
                | LPAREN expr RPAREN
                | variable
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def parse(self):
        """
        program                 : compound_statement DOT
        compound_statement      : BEGIN statement_list END
        statement_list          : statement (SEMI statement)*
        statement               : compound_statement
                                | assignment_statement
                                | empty
        assignment_statement    : variable ASSIGN expr
        empty                   : 
        variable                : ID
        expr                    : term   ((PLUS | MINUS) term)*
        term                    : factor ((MUL  | DIV) factor)*
        factor                  : unary
                                | LPAREN expr RPAREN
                                | variable
        unary                   : (PLUS | MINUS) factor
        """
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visit = getattr(self, method_name, self.error)
        return visit(node)
    
    def error(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    
    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser
    
    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
    
    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.operand) * 1
        elif node.op.type == MINUS:
            return self.visit(node.operand) * -1
    
    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)


    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''

        return self.visit(tree)

def main():
    import sys
    text = open(sys.argv[1], 'r').read()
    if len(text) <= 0:
        # sample code.
        text = """\
            BEGIN
                BEGIN
                    number := 2;
                    a := number;
                    b := 10 * a + 10 * number / 4;
                    c := a - - b
                END;
                x := 11;
            END.
        """

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()

    print(interpreter.GLOBAL_SCOPE)

if __name__ == '__main__':
    main()