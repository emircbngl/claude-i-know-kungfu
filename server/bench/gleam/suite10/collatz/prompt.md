# Task: Collatz step count

Implement a function that returns the number of steps required to reach `1` from
a positive integer `n` using the Collatz process: if `n` is even, replace it
with `n / 2`; if `n` is odd, replace it with `3 * n + 1`. `collatz(1) = 0`.

In `src/sol.gleam` (module `sol`), implement:

```gleam
pub fn collatz(n: Int) -> Int
```

Examples: `collatz(1)` = 0, `collatz(6)` = 8, `collatz(27)` = 111.
