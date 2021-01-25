## Part 8 => Include Procedure Call

If you execute the example below in the current `spi.py` file from the previous part or even from the original Ruslan's part19 repo, you'll meet with this parsing error.

```Python
    text = """
      PROGRAM Main;
        procedure Alpha;
        Begin
          WriteLn('Hello Alpha!')
        End;
      BEGIN
        Alpha;
      END.
    """
    lexer = Lexer(text)
    try:
        parser = Parser(lexer)
        tree = parser.parse()
    except (LexerError, ParserError) as e:
        print(e.message)
        sys.exit(1)

    semantic_analyzer = SemanticAnalyzer()
    try:
        semantic_analyzer.visit(tree)
    except SemanticError as e:
        print(e.message)
        sys.exit(1)

    interpreter = Interpreter(tree)
    interpreter.interpret()
```
And here's the output...

```python
>>>> Unexpected token -> Token(TokenType.SEMI, ';', position=8:12)
```
That's why we've not parsed procedures's call statement yet. So let's do it...

Let's see the current `statement()` method implementation:
```python
    def statement(self):
        """
        statement : compound_statement
                  | proccall_statement
                  | assignment_statement
                  | write
                  | writeln
                  | if_statement
                  | empty
        """
        if self.current_token.type == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type in (TokenType.WRITE, TokenType.WRITELN):
            node = self.write_statement()
        elif (self.current_token.type == TokenType.ID and self.lexer.current_char == '('):
            node = self.proccall_statement()
        elif self.current_token.type == TokenType.ID:
            node = self.assignment_statement()
        elif self.current_token.type == TokenType.IF:
            node = self.if_statement()
        else:
            node = self.empty()
        return node
```
Pretty good isn't it? That method is able to recognize pretty much statements and even Ruslan made it predictive by peeking the next token using the lexer `current_chat` as a `hack` *(nice play!)*

Our parser is complaining us because he doesn't know anything about the procedure's call structures. If you take a look to our example, we have this line `Alpha;` as a `statement` but the parser treated it as an identifier thus he called `assignment_statement()` because the `elif` branch.

The `assignment_statement()` follows the rule: `ID ASSIGN expr` thus it begins by calling `variable` method and then try to eat the `ASSIGN` TokenType and here my friends is where our error blows up because the parser is expecting an `ASSIGN` token tye and the current token in fact is `SEMI`.

What will we do then?

***

1. Change the Ruslan's hack `lexer.current_char == ')'` for the `next_token` property we created in the previous chapter.
2. Modify the `assignment_statement` recognizing branch and make it predictive too by using the `next_token` property.
3. Finally add another `elif` branch that recognize and call the `variable` method.

And that's it! Let's see what it does...

```Python
    text = """
      PROGRAM Main;
        procedure Alpha;
        Begin
          WriteLn('Hello Alpha!')
        End;
      BEGIN
        Alpha;
      END.
    """
    lexer = Lexer(text)
    try:
        parser = Parser(lexer)
        tree = parser.parse()
    except (LexerError, ParserError) as e:
        print(e.message)
        sys.exit(1)

    semantic_analyzer = SemanticAnalyzer()
    try:
        semantic_analyzer.visit(tree)
    except SemanticError as e:
        print(e.message)
        sys.exit(1)

    interpreter = Interpreter(tree)
    interpreter.interpret()
```
Okay, the parser is not complaining anymore but there's no output in the console. What did we do wrong?

Well, we did all the changes pretty well though the interpreter is not able to find the `Alpha` symbol in the program `Activation Record` and that's what well be doing in the next chapter 😋

Till then, stay safe!