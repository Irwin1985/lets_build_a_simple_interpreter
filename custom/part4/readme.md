## Part 4 => TRUE and FALSE keywords

Hi and welcome to this exciting chapter! Today we're gonna extend our lexer to support two more keywords like
`TRUE` and `FALSE` which will be the building block for boolean expressions and finally will open the
path to the very expected `IF` statement. *(yeah....!!!)*

but first let's see the list of changes we'll be doing today:

***

1. Extend the `TokenType` enumeration to support the following keywords tokens:
  * TRUE    = 'TRUE'
  * FALSE   = 'FALSE'
  * BOOLEAN = 'BOOLEAN'
  * Remember insert these tokens between 'PROGRAM' and 'END' keywords delimiters...
2. Create the `Boolean` AST node class.
3. Modify the `factor` method in order to recognize and create `Boolean` ast nodes.
4. Modify the `type_spec` method to support the `BOOLEAN` built in type.
5. Create the `BOOLEAN` built in type in the `_init_builtins` method from the `ScopedSymbolTable` class.
6. Extend the `SemanticAnalyzer` and `Interpreter` classes.

And that's it! We've supported `BOOLEAN` data types. Congrats!

Now let's try it out!

```python
    text = """
        program Main;
          var truth : boolean;
        begin
          truth := true;
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

Wow! That was really cool wasn't it? our interpreter is closing to a real Pascal subset. Now let's keep moving
to the next chapter where we'll be fixing a litle grammar implementation issue. Take care and see ya...