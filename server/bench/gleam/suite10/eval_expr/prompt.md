# Task: integer expression evaluator

Implement a function that evaluates an integer arithmetic expression given as a
string. The expression uses the operators `+ - * /` (with Gleam's integer `/`),
**standard precedence** (`*` and `/` bind tighter than `+` and `-`),
**left-associativity**, and **parentheses**. Operands are non-negative integer
literals and there are no spaces.

In `src/sol.gleam` (module `sol`), implement:

```gleam
pub fn eval_expr(s: String) -> Int
```

Examples: `eval_expr("2+3*4")` = 14, `eval_expr("(2+3)*4")` = 20,
`eval_expr("100/5/2")` = 10, `eval_expr("2+3-1")` = 4,
`eval_expr("(1+2)*(3+4)")` = 21.
