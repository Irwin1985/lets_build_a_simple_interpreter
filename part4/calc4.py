# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, MUL, DIV, EOF = 'INTEGER', 'MUL', 'DIV', 'EOF'

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, MUL, DIV, or EOF
        self.type = type
        # token value: non-negative integer value, '*', '/', or None
        self.value = value
    
    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def error():
        raise Exception('Invalid character')
    
    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        """Return a (multidigit) integer consumed from the input. """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)
    
    def get_next_token(self):
        """Lexical analizer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
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
        # this step is also known as "Look Ahead"
        self.current_token = self.lexer.get_next_token()
    
    def error():
        raise Exception('Syntax Error')
    
    def eat(self, token_type):
        # compare the current token type with the passes token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        """Return an INTEGER token value.

        factor  : integer
        """
        token = self.current_token
        self.eat(INTEGER)
        return token.value
    
    def expr(self):
        """Arithmetic expression parser / interpreter.
        expr    : factor ((MUL|DIV) factor)*
        factor  : INTEGER
        """
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

Answer the questions based on the following diagram:

expr    : factor ( ( MUL | DIV ) factor )*
factor  : INTEGER

1. What is a context-free grammar (grammar)?
    A CFG is a set of rules that describes the language's formal grammar in a compact and redable manner.

2. How many rules / productions does the grammar have?
    it has 2 rules or productions which are expr and factor.

3. What is a terminal? (Identify all terminals in the picture)
    A terminal is an atom from the alphabet of a language. It called terminal because it can't be derived
    because it is an unit itself. e.g. INTEGER, STRING, etc.

    In the grammar above `MUL, DIV and INTEGER` are terminals.

4. What is a non-terminal? (Identify all non-terminals in the picture)
    A non terminal is an element from the grammar that contains either terminals and/or non terminals elements.

    In the grammar above `expr and factor` are non terminals.

5. What is a head of a rule? (Identify all heads / left-hand sides in the picture)
    The head of any grammar (also called 'right hand side') usually is a non terminal
    element which can be composed either by terminals and/or non terminals.

    In the grammar above `expr` and `factor` are the head of their own productions.

6. What is a body of the rule? (Identify all bodies / right-hand sides in the picture)
    The body of the rule or production is composed by terminals and/or non terminals.
    they can be identified in the right hand side of the grammar.

    In the grammar below the body of the grammar are surrounded by '<<<' and '<<<'
        expr    : <<<factor ( ( MUL | DIV ) factor )*<<<
        factor  : <<<INTEGER<<<


7. What is the start symbol of a grammar?
    The starting symbol of a producction is the first rule a parser needs
    in order to `start` recognizing the grammar structure. A grammar can only contain one start symbol.

    In the grammar above: `expr` its the starting symbol.

"""