## Part 2 => Write and WriteLn statements

Hi again, today we're gonna learn how to parse and interpret the `Write` and `WriteLn` Statements. By the end of this chapter
our interpreter will be able to execute this example:

```Pascal
program Main;
begin
  WriteLn('Hello World!');
end.
```

And we'll be happy because our interpreter will talk for the first time!

Well, let's get started. As always these are the steps we need to accomplish.

***

1. Create a `TokenType` in the reserved words boundaries like WRITE = 'WRITE' and WRITELN = 'WRITELN'.
2. Create the `WriteStmt` AST node.
3. Extend the `statement` method in the `Parser` class in order to recognize the `Write` or `WriteLn` keywords.
4. Create the `write_statement` method and return the WriteStmt AST node.
5. Create the `String` AST node.
6. Extend the `factor` method in order to recognize and return the token STRING.
7. Extend the `SemanticAnalyzer` class to visit two more AST: `visit_String()` and `visit_WriteStmt()`
8. Extend the `Interpreter` class to also the `visit_String()` and `visit_WriteStmt()` methods.

Ok I know those are a bunch of changes but eventually you'll find it pretty straightforward believe me :-) moreover I commented
some changes in order to ease their comprehension.

# Well, I hope you enjoyed this chapter as much as I did. See you next time...