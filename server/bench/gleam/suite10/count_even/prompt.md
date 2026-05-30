# Task: count even numbers

Implement a function that returns how many elements of a list of integers are
even. The count for an empty list is `0`.

In `src/sol.gleam` (module `sol`), implement:

```gleam
pub fn count_even(xs: List(Int)) -> Int
```

Examples: `count_even([1, 2, 3, 4, 6])` = 3, `count_even([1, 3, 5])` = 0,
`count_even([])` = 0.
