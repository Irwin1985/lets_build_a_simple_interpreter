"""
    1. Write a grammar that describes arithmetic expressions containing any number of +, -, *, or / operators.
        expr    :   term   ( ( ADD | SUB ) term   )*
        term    :   factor ( ( MUL | DIV ) factor )*
        factor  :   INTEGER
    
    2. Using the grammar, write an interpreter that can evaluate arithmetic expressions containing any number 
       of +, -, *, or / operators. Your interpreter should be able to handle expressions like 
       “2 + 7 * 4”, “7 - 8 / 4”, “14 + 2 * 3 - 6 / 2”, and so on.

"""

# This intepreter takes any expression with the format: INTEGER ((ADD, SUB, DIV, MUL) INTEGER)*

# Tokentypes
EOF, ADD, SUB, MUL, DIV, INTEGER = 'EOF', 'ADD', 'SUB', 'MUL', 'DIV', 'INTEGER'

# Class Token
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

# Class Lexer
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0 # current input character pointer
        self.current_char = self.text[self.pos]
    
    def error():
        raise Exception('Invalid character')

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

    # get the next token on demand.
    def get_next_token(self):
        if self.current_char is None:
            return Token(EOF, None)

        if self.current_char.isspace():
            self.skip_whitespace()
        
        if self.current_char.isdigit():
            return Token(INTEGER, self.integer())
        
        if self.current_char == '+':
            self.advance()
            return Token(ADD, '+')
        
        if self.current_char == '-':
            self.advance()
            return Token(SUB, '-')
        
        if self.current_char == '*':
            self.advance()
            return Token(MUL, '*')
        
        if self.current_char == '/':
            self.advance()
            return Token(DIV, '/')
        
        self.error()

# class Parser
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token() # the look ahead token.
    
    def error():
        raise Exception('Invalid Syntax')

    def expr(self):
        result = self.term()
        while self.current_token.type in (ADD, SUB):
            token = self.current_token
            if token.type == ADD:
                self.eat(ADD)
                result += self.term()
            elif token.type == SUB:
                self.eat(SUB)
                result -= self.term()
        return result

    def term(self):
        result = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result /= self.factor()
        return result
    
    def factor(self):
        value = self.current_token.value
        self.eat(INTEGER)
        return value
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

def main():
    
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        result = parser.expr()
        print(result)

    """
    text = "5*5"
    lexer = Lexer(text)
    parser = Parser(lexer)
    result = parser.expr()
    print(result)    
    """

if __name__ == '__main__':
    main()

    
