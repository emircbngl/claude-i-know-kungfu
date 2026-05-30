# Task: count the even values among the first n elements

In a module named `Sol` (file `src/Sol.obn`), implement

```
PROCEDURE CountEven*(a: ARRAY OF INTEGER; n: INTEGER): INTEGER
```

returning how many of the first `n` elements `a[0] .. a[n-1]` are even. When
`n = 0` the count is `0`.

Examples: `CountEven([1,2,3,4,6], 5)` = 3, `CountEven([1,3,5], 3)` = 0,
`CountEven(_, 0)` = 0.

Oberon-07 cannot pass empty array literals, so the empty case is exercised with
`n = 0` against any small array.
