# Reference: iterative Fibonacci (fib(0)=0, fib(1)=1).
function fib(n)
    a, b = 0, 1
    for _ in 1:n
        a, b = b, a + b
    end
    return a
end
