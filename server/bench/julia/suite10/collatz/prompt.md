# Task: Collatz steps

In `src/sol.jl`, implement `collatz(n)` that returns, as an `Int`, the number of
steps needed to reach 1 from a positive integer `n` under the Collatz map: if `n`
is even, `n -> n/2`; if odd, `n -> 3n + 1`. `collatz(1) = 0`.

Signature: `function collatz(n)` (where `n` is a positive `Int`).

Examples: `collatz(1)` = 0, `collatz(6)` = 8, `collatz(27)` = 111.

Note: halving must use integer division (`div(n, 2)`); `/` produces a `Float64`.
