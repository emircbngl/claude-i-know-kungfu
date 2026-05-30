# Task: greatest common divisor

In a module named `Sol` (file `src/Sol.obn`), implement

```
PROCEDURE GcdOf*(a, b: INTEGER): INTEGER
```

returning the greatest common divisor of `a` and `b`. You may assume
`a >= 0` and `b >= 0`. By convention `gcd(x, 0) = x` and `gcd(0, x) = x`.

Examples: `GcdOf(12, 18)` = 6, `GcdOf(7, 0)` = 7, `GcdOf(0, 5)` = 5,
`GcdOf(17, 5)` = 1.
