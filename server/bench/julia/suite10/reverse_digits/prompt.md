# Task: reverse the digits of a number

In `src/sol.jl`, implement `reverse_digits(n)` that returns, as an `Int`, the
number formed by reversing the decimal digits of a non-negative integer `n`.
Leading zeros that result from the reversal are dropped (e.g. reversing 1230
gives 0321, i.e. 321).

Signature: `function reverse_digits(n)` (where `n` is a non-negative `Int`).

Examples: `reverse_digits(1230)` = 321, `reverse_digits(7)` = 7,
`reverse_digits(100)` = 1, `reverse_digits(0)` = 0.

Note: use integer arithmetic (`div`, `%`); `/` produces a `Float64` in Julia.
