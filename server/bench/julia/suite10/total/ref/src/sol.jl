# Reference: sum a vector of integers, returning an Int (0 for empty).
function total(xs)
    s = 0
    for x in xs
        s += x
    end
    return s
end
