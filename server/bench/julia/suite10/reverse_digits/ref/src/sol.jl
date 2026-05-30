# Reference: reverse the decimal digits of a non-negative integer.
# Uses integer arithmetic (div/%); leading zeros vanish naturally.
function reverse_digits(n)
    r = 0
    while n > 0
        r = r * 10 + n % 10
        n = div(n, 10)
    end
    return r
end
