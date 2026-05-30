# Task: integer expression evaluator (the hard one)

In `src/sol.gleam` (module `sol`), implement `pub fn eval(s: String) -> Int` that
evaluates an integer arithmetic expression string with `+ - * /` (Gleam's integer
`/`), **standard precedence** (`*`/`/` over `+`/`-`), **left-associativity**, and
**parentheses**. Non-negative integer literals, no spaces.

Examples: `eval("2+3*4")` = 14, `eval("(2+3)*4")` = 20, `eval("100/5/2")` = 10,
`eval("(1+2)*(3+4)")` = 21, `eval("2+3-1")` = 4.

This needs mutual recursion (expr → term → factor → expr). Gleam allows top-level
functions to call each other regardless of order, so — unlike the same task in
Oberon — this is structurally straightforward; the real work is the strict type
system, exhaustive `case`, and the `gleam/string` grapheme API.
