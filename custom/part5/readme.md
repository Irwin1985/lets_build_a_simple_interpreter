## Part 5 => Fixing grammar

In today's chapter we'll be fixing a litle issue about the declaration of a block. Let's see the error first.
<hr>

Let's execute this valid Pascal program and see the output:

***

```python
    text = """
        program Main;
          var truth     : boolean;
          var notTruth  : boolean;
        begin
          truth := true;
          notTruth := false;
          writeln(truth);
        end.
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
And here's the output:

```python
>>>> ParserError: Unexpected token -> Token(TokenType.VAR, 'VAR', position=4:11)
```

😨 what just happened? the `Parser` cannot parse multiple `VAR` declarations but why?. Let's see our
current grammar description from the `declarations` method.

```python
  """
  declarations : (VAR (variable_declaration SEMI)+)? procedure_declaration*
  """
```

Take a sight closer to the first grammar rule: `(VAR (variable_declaration SEMI)+)?`

This rule says: 

a `declaration` is optionally a `VAR` terminal followed by one or more `variable_declaration` 
followed by a `SEMI` terminal.

do you see the issue here? this first rule accept at least one `VAR` terminal and our example above
has 2 `VAR` tokens declarations which is a perfect `Pascal` syntax. *(try yourself in freepascal compiler)*

now that we spot the error, let's fix it shall we?

First let's fix the grammar rule in order to support more than one `VAR` declaration:

Here's the new grammar:
```python
  """
  declarations : (VAR (variable_declaration SEMI)+)+ procedure_declaration*
  """
```

Pretty strightforward isn't it?😉 we just added the `+` wildcard in order to indicate that we'll allow
one or more repetition of that rule.

Let's keep moving and tackle the grammar implementation:

Here's the original code:

```python
  if self.current_token.type == TokenType.VAR:
      self.eat(TokenType.VAR)
      while self.current_token.type == TokenType.ID:
          var_decl = self.variable_declaration()
          declarations.extend(var_decl)
          self.eat(TokenType.SEMI)
```

This code follows the grammar's rule pretty good because it only allows one `VAR` declaration and you can
see it by looking the `IF` statement which check the `VAR` token once.

Let's change the `IF` for a `WHILE`:

```python
  while self.current_token.type == TokenType.VAR:
      self.eat(TokenType.VAR)
      while self.current_token.type == TokenType.ID:
          var_decl = self.variable_declaration()
          declarations.extend(var_decl)
          self.eat(TokenType.SEMI)
```

😱 Wow, making this change was really hard don't you think? 😁

And that's it! I'm sorry disappoint you if you were expecting more changes.


Now let's try our example again and see what happens:

```python
    text = """
        program Main;
          var truth     : boolean;
          var notTruth  : boolean;
        begin
          truth := true;
          notTruth := false;
          writeln(truth);
        end.
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
And here's the output:

```python
>>>> TRUE
```

🥳 Nice! our interpreter now can parse multiple `VAR` declaration and the changes were tiny. Let's keep this attitude
in the following chapters... see you there!