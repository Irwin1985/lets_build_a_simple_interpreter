""" SPI - Simple Pascal Interpreter. Part 10."""
###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis

INTEGER         = 'INTEGER'
REAL            = 'REAL'
INTEGER_CONST   = 'INTEGER_CONST'
REAL_CONST      = 'REAL_CONST'
PLUS            = 'PLUS'
MINUS           = 'MINUS'
MUL             = 'MUL'
INTEGER_DIV     = 'INTEGER_DIV'
FLOAT_DIV       = 'FLOAT_DIV'
LPAREN          = '('
RPAREN          = ')'
ID              = 'ID'
ASSIGN          = 'ASSIGN'
BEGIN           = 'BEGIN'
END             = 'END'
SEMI            = 'SEMI'
DOT             = 'DOT'
PROGRAM         = 'PROGRAM'
VAR             = 'VAR'
COLON           = ':'
COMMA           = ','
EOF             = 'EOF'

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
            'PROGRAM': Token('PROGRAM', 'PROGRAM'),
            'VAR': Token('VAR', 'VAR'),
            'DIV': Token('FLOAT_DIV', 'DIV'),
            'INTEGER': Token('INTEGER_DIV', 'INTEGER'),
            'REAL': Token('REAL', 'REAL'),
            'BEGIN': Token('BEGIN', 'BEGIN'),
            'END': Token('END', 'END')
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
    
    def skip_comment(self):
        while self.current_char != None and self.current_char != '}':
            self.advance()
        if self.current_char == None:
            raise Exception('Unexpected End of File')
        self.advance() # skip the closing '}'

    def number(self):
        result = ''
        while self.current_char != None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.' and self.peek().isdigit():
            result += self.current_char
            self.advance() # skip the '.'
            while self.current_char != None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            return Token(REAL_CONST, float(result))
        else:
            return Token(INTEGER_CONST, int(result))
            
    
    def _id(self):
        result = ''
        while self.current_char != None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        token = self.keywords.get(result.upper(), Token(ID, result))
        return token
    
    def get_next_token(self):
        while self.current_char != None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.skip_comment()
                continue
            
            if self.current_char.isdigit():
                return self.number()
            
            if self.current_char.isalpha() or self.current_char == '_':
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
                return Token(FLOAT_DIV, "/")
            
            if self.current_char == '.':
                self.advance()
                return Token(DOT, ".")
            
            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ";")
            
            if self.current_char == ':':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(ASSIGN, ":=")
                else:
                    self.advance()
                    return Token(COLON, ":")
            
            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ",")
            
            self.error()

        return Token(EOF, None)
###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################  
class AST(object):
    pass

class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block

class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

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
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(PROGRAM)    
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(DOT)
        return program_node

    def block(self):
        """block : declarations compound_statement"""
        declaration_nodes = self.declarations()
        compound_statement = self.compound_statement()
        node = Block(declaration_nodes, compound_statement)
        return node
    
    def declarations(self):
        """declarations : VAR (variable_declaration SEMI)+ | empty"""
        declarations = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(SEMI)

        return declarations

    def variable_declaration(self):
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_nodes = [Var(self.current_token)] # first ID
        self.eat(ID)

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)
        
        self.eat(COLON)
        type_node = self.type_spec()
        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]
        return var_declarations
    
    def type_spec(self):
        """type_spec : INTEGER | REAL"""
        token = self.current_token
        self.eat(token.type)        
        return Type(token)
    
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
        """term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
        node = self.factor()
        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(node, token, self.factor())

        return node

    def factor(self):
        """
         factor : PLUS     factor
                | MINUS    factor
                | INTEGER_CONST
                | REAL_CONST
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
        elif token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type == REAL_CONST:
            self.eat(REAL_CONST)
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
    
    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        pass

    def visit_Type(self, node):
        pass

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))
    
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
    text = ""
    if len(sys.argv) > 1:
        text = open(sys.argv[1], 'r').read()
    
    if len(text) <= 0:
        # sample code.
        text = """\
            begin
                BeGIn
                    _number_ := 2;
                    a := _number_;
                    b := 10 * a + 10 * _number_ / 4;
                    c := a - - b
                End;
                x := 11;
            end.
        """

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()

    print(interpreter.GLOBAL_SCOPE)

if __name__ == '__main__':
    main()