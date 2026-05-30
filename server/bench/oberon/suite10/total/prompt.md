# Task: sum the first n elements

In a module named `Sol` (file `src/Sol.obn`), implement

```
PROCEDURE Total*(a: ARRAY OF INTEGER; n: INTEGER): INTEGER
```

returning the sum of the first `n` elements `a[0] .. a[n-1]`. When `n = 0` the
sum is `0`.

Examples: `Total([1,2,3,4], 4)` = 10, `Total(_, 0)` = 0, `Total([5], 1)` = 5.

Oberon-07 cannot pass empty array literals, so the empty case is exercised with
`n = 0` against any small array.
