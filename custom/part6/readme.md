## Part 6 => Boolean Expressions

Today we'll be supporting Boolean expressions by modifying the BinOp AST node. Let's see how is it done...

***
At the end of this chapter our parser will be able to interpret the following boolean expressions:

```pascal
  program Main;
    var a, b : integer;
  begin
    a := 1;
    b := 2;
    writeln('a > b => ', a > b);
    writeln('a < b => ', a < b);
    writeln('a = b => ', a = b);
    writeln('a >= b => ', a >= b);
    writeln('a <= b => ', a <= b);
    writeln('a <> b => ', a <> b);
  end.
```

Our lexer already knows the relational operators tokens but our parser doesn't. In order to achieve that
we first need to extend our expression grammar rule to accept arithmetics and boolean expressions.

Here's the current expression rule:

```
  expr    : term ((PLUS | MINUS) term)*
  term    : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)
  factor  : PLUS factor
          | MINUS factor
          | INTEGER_CONST
          | REAL_CONST
          | LPAREN expr RPAREN
          | TRUE
          | FALSE
          | variable
```

The above grammar belogs to `expr` *(expression)* production and it only support `Arithmetic` expressions
like:

```python
  1 + 1
  4 - 2
  3 * 8
  9 / 3
```

We need to extend it in order to support `Booleans` expressions like:

```python
  1 = 1
  4 < 2
  3 > 8
  9 <> 3
  2 = 2
```

So, how do we achieve that without breaking the current `Arithmetic` expression rule?

Here's a solution:

```
  expr            : relation
  relation        : arithmetic_expr (rel_op arithmetic_expr)?
  rel_op          : LESS_THAN
                  | GREATER_THAN
                  | EQUAL
                  | LESS_EQUAL
                  | GREATER_EQUAL
                  | NOT_EQUAL
  arithmetic_expr : term ((PLUS | MINUS) term)*
  term            : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)
  factor          : PLUS factor
                  | MINUS factor
                  | INTEGER_CONST
                  | REAL_CONST
                  | LPAREN expr RPAREN
                  | TRUE
                  | FALSE
                  | variable
```

The key here relies on the `relation` production rule because it says that a relation is an `arithmetic_expr`
optionally followed by `rel_op` followed by `arithmetic_expr`.

If we pass this expression: `5` then it is completely valid because the rule says `arithmetic_expr` goes first. The same applies to `TRUE` or `FALSE` because they are seen as a `factor` too.

Let's split the new grammar and understand every production shall we?

The starting symbol is: `Expression`
```
  expr : relation
```
![alt text](https://github.com/Irwin1985/lets_build_a_simple_interpreter/tree/main/custom/part6/expr.png)