# Reference: sum of the decimal digits of a non-negative integer.
function digit_sum(n)
    s = 0
    while n > 0
        s += n % 10
        n = div(n, 10)
    end
    return s
end
