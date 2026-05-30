# Reference: primality test by trial division up to sqrt(n).
# Returns 1 if prime, 0 otherwise.
function is_prime(n)
    if n < 2
        return 0
    end
    d = 2
    while d * d <= n
        if n % d == 0
            return 0
        end
        d += 1
    end
    return 1
end
