# Task: sum of digits

In `src/sol.jl`, implement `digit_sum(n)` that returns, as an `Int`, the sum of
the decimal digits of a non-negative integer `n`. The digit sum of 0 is 0.

Signature: `function digit_sum(n)` (where `n` is a non-negative `Int`).

Examples: `digit_sum(1234)` = 10, `digit_sum(0)` = 0, `digit_sum(99)` = 18.

Note: use integer arithmetic (`div`, `%`); `/` produces a `Float64` in Julia.
