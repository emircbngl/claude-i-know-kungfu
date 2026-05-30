# Reference: Euclidean algorithm for the GCD of two non-negative integers.
function gcd_of(a, b)
    while b != 0
        a, b = b, a % b
    end
    return a
end
