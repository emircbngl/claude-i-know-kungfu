using Test
include("../src/sol.jl")

@testset "reverse_digits" begin
    @test reverse_digits(1230) == 321
    @test reverse_digits(7) == 7
    @test reverse_digits(100) == 1
    @test reverse_digits(0) == 0
end
