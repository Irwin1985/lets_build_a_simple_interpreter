### Tokenizing Strings

Hi and welcome to this first unofficial part. Today will learn how to create string tokens 
in order to print text in the next chapters, so these are the `tasks` we need to do in the lexer class:

***

1. Create another `TokenType` enum like: STRING = 'STRING'.
2. Create one method called `string` and return the string token.
3. Modify the `get_next_token()` method in order to recognize the string delimiter.

Find the changes code in `spi.py` by looking the order of these points, for example if you want to
find the first task just need to find the region of code enclosed by `#>>part1->Task1` and so forth.

Okay, now let's test our changes:

hit the python shell and type the following:

```python
>>>> from spi import Lexer
>>>> lexer = Lexer("'Hello World!'")
>>>> tok = lexer.get_next_token()
>>>> tok
Token(TokenType.STRING, 'Hello World!', position=1:2)
```

Great! all our changes worked pretty good. Let's keep moving to the next chapter...