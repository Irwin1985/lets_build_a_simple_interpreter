## Part 7 => IF Statement

Finally we are here in the `IF` statement. Today we'll learn how to parse this statement and our parser will be able to make decisions by using this new grammar construction.

***
At the end of this chapter our interpreter will be able to interpret the following program:

```pascal
  program Main;
    var a, b : integer;
  begin
    a := 1;
    b := 2;
    if a > b then
      writeln('a is greater than b')
    else
      writeln('a is less than b');

  end.
```

Here's today's grammar:

```
if_statement    : IF condition THEN statement_list ( else_statement | elsif_statement )?
else_statement  : ELSE statement_list
elsif_statement : ELSE if_statement
```

Take a look what **starting symbol** says: an `IF` statement is an `IF` terminal followed by a `condition` followed by the `THEN` terminal followed by a `statement_list` **optionally** followed either by an `else_statement` or `elsif_statement`.

Instead of creating a rigid grammar structure like:
```
if_statement : IF condition THEN statement_list ELSE statement_list
```

I decided create the grammar in a *flexible way* by leveraging the recursiveness of the grammar itself. Why did I do such a thing? because Pascal allow flexible `IF` statement as well, let's see some examples:

```pascal
  { single structure }
  if condition then
    consequences

  { if/else example }
  if condition then
    consequences
  else
    alternatives
  
  { if/else if/ example}
  if condition then
    consequences
  else if condition2 then
    consequences2
  
  { if/else if/ else example}
  if condition then
    consequences
  else if condition2 then
    consequences2
  else
    alternatives

  { if/else if/ else if example}
  if condition then
    consequences
  else if condition2 then
    consequences2
  else if contidion3 then
    consequences3

  { if/else if/ else if/ else example}
  if condition then
    consequences
  else if condition2 then
    consequences2
  else if contidion3 then
    consequences3
  else
    alternatives
```

Can you see the pattern structure in the examples above? Take another look! see?. By looking it closer you may realize tha the only fixed structure is: `IF` condition `THEN` consequenses and the other productions are complements for this symbol. Let's do some examples...

Let's write the starting symbol:

```pascal
IF condition THEN
  consequenses
```

Good! And now let put on it the ELSE complement and see the result:

```pascal
IF condition THEN
  consequenses
ELSE
  alternatives
```

If they were mathematical formula then we could translate it into:

* **IS**  = **I**f **S**tructure
* **EC**  = **E**lse **C**omplement
* **EIC** = **E**lse **I**f **C**omplement
* **G**   = **G**grammar

Then the above example translated into this formula is:

`G = IS + EC`

Now let's add the `ELSE IF` complement into the main structure *(IS)*.

`G = IS + EIF`

Which is the same as:

```pascal
IF condition THEN
  consequenses
ELSE IF condition2 THEN
  consequenses2
```

Did you get it? I know this is crazy and no textbooks explain any formula like this but I ivented it in order to understand the flexible IF grammar Pascal provides. Once you get the correct grammar (without ambiguities) then the other challenge is represent the grammar in code and that's what we are going to do right now...

These examples are allowed by the production above:

```pascal
  program Main;
    var a, b : integer;
  begin
    a := 10;
    { Single line statement }
    if a > 1 then
      writeln('a is greater than b'); {ends here with the semi colon}
    
    { Multiple statements by using the compound_statement remenber? BEGIN->END}
    if a < 10 then
    begin
      WriteLn('Why a is less than 10?');
      WriteLn('I told you that a will never be less than 10');
      WriteLn('So fix it already... damn it!');
      a := a + 1;
      WriteLn('Much better :-)') {the semi colon in the last sentence is optional :-)}
    end;

    { Else Statement }
    if a > 10 then
      WriteLn('Nice, I like everything grater than 10')
    else
      WriteLn('Fix it again and dont make me lose my money!'); {this unique semi colon finishes the whole sentence}
    
  end.
```

Now, why did I use `statement_list` instead of `compound_statement` one? because Pascal allow us to write one single statement without explicitly surround it with `BEGIN` and `END` block. If you need more than one statement *(see examples above)* then you are gonna put it all inside a block of statements which in our case is the `compound_statement` production. 

`statement_list` production will fit perfectly in the IF grammar because `statement_list` could contain a `compound_statement` inside of it which is great for us.

Let's recall the `statement_list` production:

```
  statement_list : statement (SEMI statement)*
  statement      : compound_statement
                 | proccall_statement
                 | assignment_statement
                 | empty
```
This grammar will make our life easier with the future grammar we'll define.

Now let's view all the changes we'll need to do in order to support `IF` statements.

***

1. Extend the `TokenType` enumeration to support the following keywords tokens:
  * IF   = 'IF'
  * THEN = 'THEN'
  * ELSE = 'ELSE'
  * Remember insert these tokens between 'PROGRAM' and 'END' keywords delimiters...
2. Create the `IfStmt` AST node class.
3. Extend the `get_next_token` method of the `Parser` and include the `next_token` property.
4. Modify the `statement` method in order to recognize and create `IfStmt` ast nodes.
5. Implement the `if_statement` grammar by creating the same method and following the rules.
6. Implement the `visit_IfStmt` method in the `SemanticAnalyzer` class.
7. Implement the `visit_IfStmt` method in the `Interpreter` class.

And that's it! Let's see what it does...

```python
    text = """
    program Main;
        var a, b : integer;
    begin
        a := 12;
        if a = 1 then
          begin
            writeln('this is the if 1...');
          end
        else if a = 2 then
          begin
            writeln('this is the if 2...');
          end
        else if a = 3 then
          begin
            writeln('this is the if 3...');
          end
        else if a = 4 then
          begin
            writeln('this is the if 4...');
          end
        else if a = 5 then
          begin
            writeln('this is the if 5...');
          end
        else if a = 6 then
          begin
            writeln('this is the if 6...');
          end
        else if a = 7 then
          begin
            writeln('this is the if 7...');
          end
        else
            if a = 12 then
                write('It is 12! Yeah baby...!!! BTW: this is a nested If... pretty cool eh...?')
            else
                write('I dont know what is it :(');
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

And here's the output...

```python
>>>> It is 12! Yeah baby...!!! BTW: this is a nested If... pretty cool eh...?
```

🥳 Superb! if you did all these steps and your interpreter version is running the same result then congratulations!. Take your time to read the implementation code and make sure you can understand every single step. Today we gave a giantic step into Compilers and Interpreters world! Our main goal is closer than ever so let's keep moving...