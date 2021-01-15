from enum import Enum

class TokenType(Enum):
    # single-character token types
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    FLOAT_DIV = '/'
    LPAREN = '('
    RPAREN = ')'
    SEMI = ';'
    DOT = '.'
    COLON = ':'
    COMMA = ','
    # block of reserved words
    PROGRAM = 'PROGRAM'
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    INTEGER_DIV = 'DIV'
    VAR = 'VAR'
    PROCEDURE = 'PROCEDURE'
    BEGIN = 'BEGIN'
    END = 'END' 
    # misc
    ID = 'ID'
    INTEGER_CONST = 'INTEGER_CONST'
    REAL_CONST = 'REAL_CONST'
    ASSIGN = ':='
    EOF = 'EOF'

char = '#'
try:
    token = TokenType(char)
except ValueError:
    print("Unknown character: " + char)
else:
    print(token)

# lista = list(TokenType)
# for type in lista:
#     print('name:{name}, value: {value}'.format(name = type.name, value = type.value))

# tt_list = list(TokenType)
# start_index = tt_list.index(TokenType.PROGRAM)
# end_index = tt_list.index(TokenType.END)

# reserved_keywords = {
#     token_type.value: token_type
#     for token_type in tt_list[start_index:end_index+1]
# }
# print(reserved_keywords)