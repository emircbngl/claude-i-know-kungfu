# Task: sum a list of integers

Implement a function that returns the sum of a list of integers. The sum of an
empty list is `0`.

In `src/sol.gleam` (module `sol`), implement:

```gleam
pub fn total(xs: List(Int)) -> Int
```

Examples: `total([1, 2, 3, 4])` = 10, `total([])` = 0, `total([5])` = 5.
