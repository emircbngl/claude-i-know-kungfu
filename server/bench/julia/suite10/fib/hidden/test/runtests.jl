using Test
include("../src/sol.jl")

@testset "fib" begin
    @test fib(0) == 0
    @test fib(1) == 1
    @test fib(10) == 55
    @test fib(20) == 6765
end
