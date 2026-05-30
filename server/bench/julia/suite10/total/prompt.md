# Task: sum a vector

In `src/sol.jl`, implement `total(xs)` that returns the sum of a vector of
integers as an `Int`. The sum of an empty vector is `0`.

Signature: `function total(xs)` (where `xs` is a `Vector{Int}`).

Examples: `total([1, 2, 3, 4])` = 10, `total(Int[])` = 0, `total([5])` = 5.

Note: do not name it `sum` — that clashes with Julia's `Base.sum` and redefining
it errors.
