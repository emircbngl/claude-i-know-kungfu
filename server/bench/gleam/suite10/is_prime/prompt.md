# Task: primality test

Implement a function that returns `1` if `n` is prime and `0` otherwise. By
definition, numbers less than `2` are not prime.

In `src/sol.gleam` (module `sol`), implement:

```gleam
pub fn is_prime(n: Int) -> Int
```

Examples: `is_prime(2)` = 1, `is_prime(7)` = 1, `is_prime(9)` = 0,
`is_prime(1)` = 0, `is_prime(13)` = 1.
