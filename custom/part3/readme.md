## Part 3 => Relational Operators

Today we're gonna extend our lexer to support relational operators such as: `<, >, =, <=, >=, <>` and here is the list
of changes we'll do:

***

1. Extend the `TokenType` enumeration to support the following tokens:
  * LESS_THAN     = '<'
  * GREATER_THAN  = '>'
  * EQUAL         = '='
  * LESS_EQUAL    = '<='
  * GREATER_EQUAL = '>='
  * NOT_EQUAL     = '<>'

Okay that was pretty easy wasn't it?, now let's try it out.

```python
    text = """
      { some relational expressions }
      a > b;
      5 <= 7;
      b < c;
      c <> a;
      a = b;
    """
    try:
        tok = lexer.get_next_token()
        while tok.type != TokenType.EOF:
            print(repr(tok))
            tok = lexer.get_next_token()            
    except (LexerError) as e:
        print(e.message)
        sys.exit(1)        
```
And here's the output:

```python
>>>> Token(TokenType.ID, 'a', position=3:7)
>>>> Token(TokenType.GREATER_THAN, '>', position=3:9)     
>>>> Token(TokenType.ID, 'b', position=3:11)
>>>> Token(TokenType.SEMI, ';', position=3:12)
>>>> Token(TokenType.INTEGER_CONST, 5, position=4:7)      
>>>> Token(TokenType.LESS_EQUAL, '<=', position=4:9)      
>>>> Token(TokenType.INTEGER_CONST, 7, position=4:12)
>>>> Token(TokenType.SEMI, ';', position=4:13)
>>>> Token(TokenType.ID, 'b', position=5:7)
>>>> Token(TokenType.LESS_THAN, '<', position=5:9)
>>>> Token(TokenType.ID, 'c', position=5:11)
>>>> Token(TokenType.SEMI, ';', position=5:12)
>>>> Token(TokenType.ID, 'c', position=6:7)
>>>> Token(TokenType.NOT_EQUAL, '<>', position=6:9)
>>>> Token(TokenType.ID, 'a', position=6:12)
>>>> Token(TokenType.SEMI, ';', position=6:13)
>>>> Token(TokenType.ID, 'a', position=7:7)
>>>> Token(TokenType.EQUAL, '=', position=7:9)
>>>> Token(TokenType.ID, 'b', position=7:11)
>>>> Token(TokenType.SEMI, ';', position=7:12)
```

Well, that's all for today's chapter! In the next one well be supporting `TRUE` and `FALSE` keywords...