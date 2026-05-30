# Reference: count the even integers in a vector.
function count_even(xs)
    c = 0
    for x in xs
        if x % 2 == 0
            c += 1
        end
    end
    return c
end
