# Task: integer expression evaluator (the hard one)

In a module named `Sol` (file `src/Sol.obn`), implement

```
PROCEDURE EvalExpr*(s: ARRAY OF CHAR): INTEGER
```

that evaluates an integer arithmetic expression string supporting the four
operators `+ - * /` (integer `DIV`), **standard precedence** (`*` and `/` bind
tighter than `+` and `-`), **left-associativity**, and **parentheses**.
Operands are non-negative integer literals; there are no spaces.

Examples: `EvalExpr("2+3*4")` = 14, `EvalExpr("(2+3)*4")` = 20,
`EvalExpr("100/5/2")` = 10, `EvalExpr("2+3-1")` = 4,
`EvalExpr("(1+2)*(3+4)")` = 21.

This needs mutually recursive parsing (expr → term → factor → expr), which is
the sharp edge of Oberon-07: it has **no forward declarations**, and OBNC also
forbids calling a *sibling* nested procedure and accessing an enclosing
procedure's locals. A first attempt that reaches for `FORWARD` or flat mutual
recursion will not compile. The clean approach that compiles is a **procedure
variable** at module level: declare `TYPE EP = PROCEDURE(): INTEGER; VAR expr:
EP;`, assign `expr := Expr` inside `EvalExpr`, and have `Factor` call `expr()`
indirectly. Parser state (`src`, `pos`) lives in module globals.
