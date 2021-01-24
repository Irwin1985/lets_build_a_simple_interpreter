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
3. Modify the `statement` method in order to recognize and create `IfStmt` ast nodes.
4. Implement the `if_statement` grammar by creating the same method and following the rules.
5. Implement the `visit_IfStmt` method in the `SemanticAnalyzer` class.
6. Implement the `visit_IfStmt` method in the `Interpreter` class.

And that's it! Let's see what it does...

