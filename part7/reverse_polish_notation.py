"""
    Write a translator (hint: node visitor) that takes as input an arithmetic expression and 
    prints it out in postfix notation, also known as Reverse Polish Notation (RPN). 
    For example, if the input to the translator is the expression (5 + 3) * 12 / 3 than the 
    output should be 5 3 + 12 * 3 /. See the answer here but try to solve it first on your own.
"""
INTEGER, PLUS, MINUS, DIV, MUL, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'DIV', 'MUL', 'LPAREN', 'RPAREN', 'EOF'
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
    
    def error(self):
        raise Exception('Unknown character')
    
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, ")")
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
        self.value = self.token.value

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self):
        raise Exception('Syntax Error.')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
        else:
            node = Num(self.current_token)
            self.eat(INTEGER)
        return node
    
    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(node, token, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(node, token, self.term())
        return node
    
    def parse(self):
        return self.expr()

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visit = getattr(self, method_name, self.error)
        return visit(node)

    def error(self, node):
        raise Exception('No visitable method found in node.')

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit_BinOp(self, node):
        return '({left} {right} {op})'.format(
            left = str(self.visit(node.left)),
            right = str(self.visit(node.right)),
            op = node.op.value
        )
    
    def visit_Num(self, node):
        return node.value

def main():
    while True:
        try:
            text = input('psi> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)

if __name__ == '__main__':
    main()

