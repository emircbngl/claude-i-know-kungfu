using Test
include("../src/sol.jl")

@testset "digit_sum" begin
    @test digit_sum(1234) == 10
    @test digit_sum(0) == 0
    @test digit_sum(99) == 18
end
