# Task: maximum of a non-empty vector

In `src/sol.jl`, implement `largest(xs)` that returns the largest element of a
non-empty vector of integers as an `Int`.

Signature: `function largest(xs)` (where `xs` is a non-empty `Vector{Int}`).

Examples: `largest([3, 1, 2])` = 3, `largest([5])` = 5, `largest([4, 4, 4])` = 4.

Note: do not name it `maximum` — that clashes with `Base.maximum` and redefining
it errors.
