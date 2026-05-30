# Task: greatest common divisor

In `src/sol.jl`, implement `gcd_of(a, b)` that returns the greatest common
divisor of two non-negative integers `a, b` as an `Int`. By convention
`gcd_of(n, 0) == n` and `gcd_of(0, n) == n`.

Signature: `function gcd_of(a, b)`.

Examples: `gcd_of(12, 18)` = 6, `gcd_of(7, 0)` = 7, `gcd_of(0, 5)` = 5,
`gcd_of(17, 5)` = 1.

Note: do not name it `gcd` — that clashes with `Base.gcd` and redefining it
errors.
