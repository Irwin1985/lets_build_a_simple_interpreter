# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MUL, DIV, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF'
)

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, MUL, DIV, or EOF
        self.type = type
        # token value:  non-negative integer value, '+', '-', '*', '/', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type = self.type,
            value = self.value
        )
    
    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text# self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')
    
    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
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
            
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
            self.error()
        
        return Token(EOF, None)

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        # this is also known as 'look ahead' token.
        self.current_token = self.lexer.get_next_token()

    def error():
        raise Exception('Syntax Error')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        """factor : INTEGER"""
        token = self.current_token
        self.eat(INTEGER)
        return token.value
    
    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                divisor = self.factor()
                if divisor == 0:
                    raise Exception('division by zero.')
                result = result / divisor
        
        return result
    
    def expr(self):
        """Arithmetic expression parser / interpreter.

        calc> 14 + 2 * 3 - 6 / 2
        17

        expr    :   term   ((PLUS | MINUS)   term  )*
        term    :   factor ((MUL  | DIV)     factpr)*
        factor  :   INTEGER
        """
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        
        return result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()

"""
Check your understanding

**DISCLAIMER**
    I answer all in English but keep in mind I'm not a native English speaker thus there will be 
    grammars and semantics errors (that's funny because I'm learning formal language grammar)

 1. What does it mean for an operator to be left-associative?
    It means that it belogs to the left most operand. For example:
    5 - 3 - 2
    in order to effectively parse this expression, the parser must check the '-' operator associativity 
    givin this result: (5 - 3) - 2 instead of: 5 - (3 - 2) thus associativity exists to prevent ambiguities.

2. Are operators + and - left-associative or right-associative? What about * and / ?
    '+' and '-' operators are left associative
    '*' and '/' operators are left associative

3. Does operator + have higher precedence than operator * ?
    No. Based on the precedence table. '+' operator has lower precedence than '*'.
 """