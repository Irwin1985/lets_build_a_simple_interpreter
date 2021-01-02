# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, STAR, SLASH, EOF = 'INTEGER', 'PLUS', 'MINUS', 'STAR', 'SLASH', 'EOF'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF.
        self.type = type
        # token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.
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
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """ Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # eat white spaces
        while not self.is_at_end() and self.text[self.pos].isspace():
            if self.is_at_end():
                return Token(EOF, None)
            self.pos += 1

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.is_at_end():
            return Token(EOF, None)


        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]
        self.pos += 1

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():            
            token_str = current_char
            if not self.is_at_end():
                current_char = text[self.pos]
                # alterar el lexer para que reconozca digitos largos.
                while current_char.isdigit():
                    token_str += text[self.pos]
                    self.pos += 1
                    if self.pos <= (len(self.text)-1):
                        current_char = text[self.pos]
                    else:
                        break
                # fin

            token = Token(INTEGER, int(token_str))
            return token

        token_type = EOF
        if current_char == '+':
            token_type = PLUS            
        elif current_char == '-':
            token_type = MINUS
        elif current_char == '*':
            token_type = STAR
        elif current_char == '/':
            token_type = SLASH
        else:
            self.error()

        return Token(token_type, current_char)

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):
        """ expr -> INTEGER PLUS INTEGER """
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)

        # we expect the current token to be a '+' token
        op = self.current_token
        self.eat(self.current_token.type)

        # we expect the current token to be a single-figit integer
        right = self.current_token
        self.eat(INTEGER)

        # after the above call the self.current_token is set to
        # EOF token

        # at this point INTEGER PLUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding two integers, thus
        # effectively interpreting client input
        result = 0.00
        if op.value == '+':
            result = left.value + right.value
        elif op.value == '-':
            result = left.value - right.value
        elif op.value == '*':
            result = left.value * right.value
        else:
            if right.value == 0:
                raise Exception('division by zero.')
            result = left.value / right.value

        return result
    # helper methods
    def is_at_end(self):
        return self.pos >= len(self.text)

def main():
    print('<<Welcome to the first exercise of lsbasi>>')
    print('please type some input with the format: number operator number:')
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

1. What is an interpreter?
    A interpreter is a piece of software that takes an input written in some high level language (source program)
    and execute them one by one.
2. What is a compiler?
    A compiler is a piece of software that takes an input written in some high level language (source program)
    and translates it into an equivalent low level program (target program) for later execution.

3. What’s the difference between an interpreter and a compiler?
    An interpreter executes the source program sentence by sentence while a compiler translates the source program
    into another program commonly a low level program.

4. What is a token?
    A token is a related unit that represents an atom from the alphabet of certain language. It take at least two
    piece of information (attributes):
    1. a type representing the category of the related atom.
    2. a value commonly called `lexeme` that represent the symbol or word related to it.

5. What is the name of the process that breaks input apart into tokens?
    Tokenization

6. What is the part of the interpreter that does lexical analysis called?
    Lexical Analizer

7. What are the other common names for that part of an interpreter or a compiler?
    Tokenizer, Scanner, Lexer
"""