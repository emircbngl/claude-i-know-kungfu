# Task: evaluate an integer expression

In `src/sol.jl`, implement `eval_expr(s::AbstractString)` that parses and
evaluates an arithmetic expression over non-negative integer literals and the
operators `+`, `-`, `*`, `/`, with parentheses. It returns an `Int`.

Rules:
- `*` and `/` bind tighter than `+` and `-` (standard precedence).
- Operators of equal precedence are left-associative
  (e.g. `100/5/2` = `(100/5)/2`).
- `/` is **integer** division — use `div(a, b)`, NOT `/` (which yields a Float).
- Parentheses override precedence.
- The input is well-formed; you may assume no spaces matter (handle or ignore
  them).

Signature: `function eval_expr(s::AbstractString)`.

Examples: `eval_expr("2+3*4")` = 14, `eval_expr("(2+3)*4")` = 20,
`eval_expr("100/5/2")` = 10, `eval_expr("2+3-1")` = 4,
`eval_expr("(1+2)*(3+4)")` = 21.
