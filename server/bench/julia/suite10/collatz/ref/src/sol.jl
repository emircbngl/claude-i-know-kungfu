# Reference: number of Collatz steps to reach 1 (collatz(1) = 0).
# Halving uses integer division so the value stays an Int.
function collatz(n)
    steps = 0
    while n != 1
        if n % 2 == 0
            n = div(n, 2)
        else
            n = 3 * n + 1
        end
        steps += 1
    end
    return steps
end
