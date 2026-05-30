# Task: Collatz step count

In a module named `Sol` (file `src/Sol.obn`), implement

```
PROCEDURE Collatz*(n: INTEGER): INTEGER
```

returning the number of steps to reach `1` under the Collatz map: if `n` is even
replace it with `n DIV 2`, otherwise replace it with `3*n + 1`; count each
replacement as one step. By definition `Collatz(1) = 0`. You may assume
`n >= 1`.

Examples: `Collatz(1)` = 0, `Collatz(6)` = 8, `Collatz(27)` = 111.
