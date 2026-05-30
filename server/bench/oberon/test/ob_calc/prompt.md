# Task: integer expression evaluator (the hard one)

In a module named `Sol` (file `src/Sol.obn`), implement
`PROCEDURE Eval*(s: ARRAY OF CHAR): INTEGER` that evaluates an integer arithmetic
expression string supporting the four operators `+ - * /` (integer `DIV`),
**standard precedence** (`*`/`/` bind tighter than `+`/`-`), **left-associativity**,
and **parentheses**. Non-negative integer literals, no spaces.

Examples: `Eval("2+3*4")` = 14, `Eval("(2+3)*4")` = 20, `Eval("100/5/2")` = 10,
`Eval("(1+2)*(3+4)")` = 21.

This needs mutually recursive parsing (expr → term → factor → expr), which is the
sharp edge of Oberon-07: it has **no forward declarations**, and OBNC also forbids
calling a *sibling* nested procedure and accessing an enclosing procedure's locals.
A first attempt that reaches for `FORWARD` or flat mutual recursion will not
compile — which is exactly what the verify loop is for.
