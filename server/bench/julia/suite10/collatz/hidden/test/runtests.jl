using Test
include("../src/sol.jl")

@testset "collatz" begin
    @test collatz(1) == 0
    @test collatz(6) == 8
    @test collatz(27) == 111
end
