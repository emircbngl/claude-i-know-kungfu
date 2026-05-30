# Task: reverse the digits of a number

Implement a function that returns the integer formed by reversing the decimal
digits of a non-negative integer `n`. Leading zeros that result from the
reversal are dropped (they are simply not significant in the resulting integer).

In `src/sol.gleam` (module `sol`), implement:

```gleam
pub fn reverse_digits(n: Int) -> Int
```

Examples: `reverse_digits(1230)` = 321, `reverse_digits(7)` = 7,
`reverse_digits(100)` = 1, `reverse_digits(0)` = 0.
