""" SPI - Simple Pascal Interpreter. Part 13. """

###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER       = 'INTEGER'
REAL          = 'REAL'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST    = 'REAL_CONST'
PLUS          = 'PLUS'
MINUS         = 'MINUS'
MUL           = 'MUL'
INTEGER_DIV   = 'INTEGER_DIV'
FLOAT_DIV     = 'FLOAT_DIV'
LPAREN        = 'LPAREN'
RPAREN        = 'RPAREN'
ID            = 'ID'
ASSIGN        = 'ASSIGN'
BEGIN         = 'BEGIN'
END           = 'END'
SEMI          = 'SEMI'
DOT           = 'DOT'
PROGRAM       = 'PROGRAM'
VAR           = 'VAR'
COLON         = 'COLON'
COMMA         = 'COMMA'
PROCEDURE     = 'PROCEDURE'
EOF           = 'EOF'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'VAR': Token('VAR', 'VAR'),
    'DIV': Token('INTEGER_DIV', 'DIV'),
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'REAL': Token('REAL', 'REAL'),
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
    'PROCEDURE': Token('PROCEDURE', 'PROCEDURE'),
}

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()  # the closing curly brace

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while (
                self.current_char is not None and
                self.current_char.isdigit()
            ):
                result += self.current_char
                self.advance()

            token = Token('REAL_CONST', float(result))
        else:
            token = Token('INTEGER_CONST', int(result))

        return token

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result.upper(), Token(ID, result))
        return token

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

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
                return Token(FLOAT_DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            self.error()

        return Token(EOF, None)

###############################################################################
#                                                                             #
#  AST                                                                        #
#                                                                             #
###############################################################################
class AST:
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

class ProcedureDecl(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Compound(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass
###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Syntax error near of: %s' % repr(self.current_token))

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        # program ::= 'PROGRAM' variable ';' block '.'
        self.eat(PROGRAM)
        name = self.variable().value
        self.eat(SEMI)
        block = self.block()
        self.eat(DOT)
        return Program(name, block)

    def block(self):
        # block ::= declarations compound_statement
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        return Block(declarations, compound_statement)

    def declarations(self):
        # declarations ::= (var_section)* | (proc_section)* | empty
        declarations = []
        while self.current_token.type == VAR:
            declarations.extend(self.var_section())
            # self.eat(VAR)
            # while self.current_token.type == ID:
            #     var_decl = self.variable_declaration()
            #     declarations.extend(var_decl)
            #     self.eat(SEMI)

        while self.current_token.type == PROCEDURE:
            declarations.append(self.proc_section())
            # self.eat(PROCEDURE)
            # proc_name = self.current_token.value
            # self.eat(ID)
            # self.eat(SEMI)
            # block_node = self.block()
            # proc_decl = ProcedureDecl(proc_name, block_node)
            # declarations.append(proc_decl)
            # self.eat(SEMI)
        
        return declarations

    def var_section(self):
        # var_section ::= 'VAR' (variable_declaration)+
        var_nodes = []
        self.eat(VAR)
        while self.current_token.type == ID:
            var_nodes.extend(self.variable_declaration())

        return var_nodes
    def variable_declaration(self):
        # variable_declaration ::= variable (',' variable)* ':' type_spec ';'
        var_nodes = [Var(self.current_token)]
        self.eat(ID)

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)

        self.eat(COLON)

        type_node = self.type_spec()
        self.eat(SEMI)

        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]
        return var_declarations

    def type_spec(self):
        # type_spec ::= 'INTEGER' | 'REAL'
        token = self.current_token
        if token.type in (INTEGER, REAL):
            self.eat(token.type)
        else:
            raise Exception('Expected INTEGER|REAL got %s' % repr(token))
        return Type(token)

    def proc_section(self):
        # proc_section ::= 'PROCEDURE' variable ';' block ';'
        self.eat(PROCEDURE)
        name = self.variable().value
        self.eat(SEMI)
        block = self.block()
        self.eat(SEMI)
        return ProcedureDecl(name, block)

    def compound_statement(self):
        # compound_statement ::= 'BEGIN' statement_list 'END'
        self.eat(BEGIN)
        statement_list = self.statement_list()
        self.eat(END)

        root = Compound()
        for statement in statement_list:
            root.children.append(statement)

        return root

    def statement_list(self):
        # statement_list ::= statement (SEMI statement)*
        stmt = self.statement()
        results = [stmt]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        return results

    def statement(self):
        # statement_list ::= compound_statement | assign_statement | empty
        if self.current_token.type == BEGIN:
            statement = self.compound_statement()
        elif self.current_token.type == ID:
            statement = self.assign_statement()
        else:
            statement = self.empty()
        return statement  

    def assign_statement(self):
        # assign_statement ::= variable ':=' expr
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return Assign(left, token, right)

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()

    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(node, token, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(node, token, self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return UnaryOp(token, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(token, self.factor())
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type == REAL_CONST:
            self.eat(REAL_CONST)
            return Num(token)
        else:
            return self.variable()

    def parse(self):
        tree = self.program()
        if self.current_token.type != EOF:
            self.error()
        return tree
###############################################################################
#                                                                             #
#  SYMBOLS, TABLES, SEMANTIC ANALYSIS                                         #
#                                                                             #
###############################################################################
class Symbol(object):
    def __init__(self, name, type = None):
        self.name = name
        self.type = type

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name = self.__class__.__name__,
            name = self.name
        )

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)
    
    def __str__(self):
        return "<{class_name}(name='{name}','type={type}')>".format(
            class_name = self.__class__.__name__,
            name = self.name,
            type = self.type
        )
    __repr__ = __str__

class SymbolTable:
    def __init__(self):
        self._symbols = {}
        self._init_builtins()
    
    def _init_builtins(self):
        self.insert(BuiltinTypeSymbol('INTEGER'))
        self.insert(BuiltinTypeSymbol('REAL'))
    
    def __str__(self):
        symtab_header = 'Symbol table contents'
        lines = ['\n', symtab_header, '_' * len(symtab_header)]
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s
    
    __repr__ = __str__
    
    def insert(self, symbol):
        print('Insert: %s' % symbol.name)
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        return symbol

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

###############################################################################
#                                                                             #
#  CHEQUEO SEMANTICO                                                          #
#                                                                             #
###############################################################################
class SemanticAnalizer(NodeVisitor):
    def __init__(self):
        self.symtab = SymbolTable()

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_VarDecl(self, node):        
        type_name = node.type_node.value
        type_symbol = self.symtab.lookup(type_name)

        var_name = node.var_node.value
        if self.symtab.lookup(var_name) is not None:
            raise Exception(
                "Error: Duplicated identifier '%s' found" % var_name
            )
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symtab.insert(var_symbol)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise Exception(
                "Error: Symbol(identifier) not found '%s'" % var_name
            )

    def visit_Assign(self, node):
        self.visit(node.right)
        self.visit(node.left)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_NoOp(self, node):
        pass