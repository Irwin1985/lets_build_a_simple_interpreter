# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis


INTEGER, PLUS, MINUS, STAR, SLASH, EOF = 'INTEGER', 'PLUS', 'MINUS', 'STAR', 'SLASH', 'EOF'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, or EOF
        self.type = type
        # TOKEN VALUE: NON-NEGATIVE INTEGER VALUE, '+', '-', OR None
        self.value = value

    def __str__(self):
        """ String representation of the class instance.

        Examples:
        Token(INTEGER, 3)
        Token(PLUS, '+')        
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )
    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3 + 5", "12 - 5 + 3", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    ###########################################################
    # Lexer code
    ###########################################################
    def error():
        raise Exception('Invalid syntax.')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable. """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        """Return a (multidit) integer consumed from the input. """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible form breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '*':
                self.advance()
                return Token(STAR, '*')

            if self.current_char == '/':
                self.advance()
                return Token(SLASH, '*')

            self.error()

        return Token(EOF, None)

    ###########################################################
    # Parser / Interpreter code
    ###########################################################    
    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        """Return an INTEGER token value."""
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        """Arithmetic expression parser / interpreter."""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        result = self.term()
        while self.current_token.type in (STAR, SLASH):
            token = self.current_token
            if token.type == STAR:
                self.eat(STAR)
                result = result * self.term()
            elif token.type == SLASH:
                self.eat(SLASH)
                result = result / self.term()
        
        return result

def main():
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

1. What is a syntax diagram?
    A syntax diagram is a visual representation of some language's grammar rules that is easy to read an code.

2. What is syntax analysis?
    Syntax analysis is the process that recognize the grammar of a given language's rules. If the stream of 
    tokens matches the grammar then the parser continue the process, otherwise raise an syntax error.

3. What is a syntax analyzer?
   Syntax Analizer or Parser is the piece of a compiler or interpreter that create an Abstract syntax tree out of 
   the stream of token provided by the lexer. This process ensures that the language's grammar rules matches the
   tokens in order to effectively parse the tokens.
"""