# Task: reverse the decimal digits

In a module named `Sol` (file `src/Sol.obn`), implement

```
PROCEDURE ReverseDigits*(n: INTEGER): INTEGER
```

returning the integer formed by reversing the decimal digits of `n`. You may
assume `n >= 0`. Leading zeros that appear after reversal vanish (they are not
significant), so `ReverseDigits(1230) = 321` and `ReverseDigits(100) = 1`.

Examples: `ReverseDigits(1230)` = 321, `ReverseDigits(7)` = 7,
`ReverseDigits(100)` = 1, `ReverseDigits(0)` = 0.
