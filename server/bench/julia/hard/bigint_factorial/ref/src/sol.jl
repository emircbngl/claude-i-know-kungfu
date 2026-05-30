# Reference: arbitrary-precision factorial. `big(n)` makes factorial use BigInt,
# so the result is exact for n far beyond Int64's range (21! already overflows).
fact(n) = factorial(big(n))
