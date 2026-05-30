# Reference: largest element of a non-empty vector of integers.
function largest(xs)
    m = xs[1]
    for x in xs
        if x > m
            m = x
        end
    end
    return m
end
