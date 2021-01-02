# Token types
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
from os import stat_result


INTEGER, PLUS, MINUS, STAR, SLASH, EOF = 'INTEGER', 'PLUS', 'STAR', 'MINUS', 'SLASH', 'EOF'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, or EOF
        self.type = type
        # token value: non-negative integer value, '+', '-', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3 + 5", "12 - 5", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error():
        raise Exception('Error parsing input');

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
        
    def integer(self):
        """Return a (multidigit) integer consumer from the input. """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            token_type = None
            lexeme = None
            if self.current_char == '+':
                token_type = PLUS
                lexeme = '+'
            elif self.current_char == '-':
                token_type = MINUS
                lexeme = '-'
            elif self.current_char == '*':
                token_type = STAR
                lexeme = '*'
            elif self.current_char == '/':
                token_type = SLASH
                lexeme = '/'
            else:
                self.error()
            
            self.advance()
            return Token(token_type, lexeme)
        
        return Token(EOF, None)

    def eat(self, token_type):
        # compare the current token type with the passes token
        # type and if they match then "eat" the current token
        # and assignthe next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):
        """Parser / Interpreter
        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be an integer
        result = self.current_token.value
        self.eat(INTEGER)

        # handle addition and subtract.
        while self.current_token.type in [PLUS, MINUS]:
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                result += self.current_token.value
            elif self.current_token.type == MINUS:
                self.eat(MINUS)
                result -= self.current_token.value
            self.eat(INTEGER)
        
        return result


        # we expect the current token to be either a '+' or '-'

        """
        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        elif op.type == MINUS:
            self.eat(MINUS)
        elif op.type == STAR:
            self.eat(STAR)
        elif op.type == SLASH:
            self.eat(SLASH)
        """
        
        # WE EXPECT THE CURRENT TOKEN TO BE AN INTEGER
        # right = self.current_token
        # self.eat(INTEGER)
        # after the above call the self.current_token is ser to
        # EOF token

        # at this point either the INTEGER PLUS INTEGER or
        # the INTEGER MINUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding or subtracting two integers,
        # thus effectively interpreting client input
"""
        result = 0.00
        if op.type == PLUS:
            result = left.value + right.value
        elif op.type == MINUS:
            result = left.value - right.value
        elif op.type == STAR:
            result = left.value * right.value
        elif op.type == SLASH:
            if right.value == 0:
                raise Exception('division by zero.')
            else:
                result = left.value / right.value
        return result
"""

def main():
    # REPL
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()

"""
Check your understanding

**DISCLAIMER**
    I answer all in English but keep in mind I'm not a native English speaker thus there will be 
    grammars and semantics errors (that's funny because I'm learning formal language grammar)

1. What is a lexeme?
    A lexeme is a stream of related characters that represent the current token value.

2. What is the name of the process that finds the structure in the stream of tokens, or put differently, 
   what is the name of the process that recognizes a certain phrase in that stream of tokens?
   Parsing

3. What is the name of the part of the interpreter (compiler) that does parsing?
   Syntax Analizer or Parser
"""