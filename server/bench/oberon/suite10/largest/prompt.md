# Task: largest of the first n elements

In a module named `Sol` (file `src/Sol.obn`), implement

```
PROCEDURE Largest*(a: ARRAY OF INTEGER; n: INTEGER): INTEGER
```

returning the maximum among the first `n` elements `a[0] .. a[n-1]`. You may
assume `n >= 1`.

Examples: `Largest([3,1,2], 3)` = 3, `Largest([5], 1)` = 5,
`Largest([4,4,4], 3)` = 4.
