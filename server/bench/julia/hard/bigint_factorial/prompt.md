# Task: exact factorial (the hard one)

In `src/sol.jl`, implement `fact(n)` that returns the exact value of `n!` for `n`
up to 50. Examples: `fact(5)` = 120, `fact(0)` = 1.

The trap: `21!` already exceeds `Int64`, and `50!` has 65 digits. A naive `Int`
loop overflows silently and `factorial(n)` throws `OverflowError` for `n > 20`.
The exact answer needs arbitrary precision — Julia's `BigInt` (`big(n)`).
