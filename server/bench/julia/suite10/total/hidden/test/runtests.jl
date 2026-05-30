using Test
include("../src/sol.jl")

@testset "total" begin
    @test total([1, 2, 3, 4]) == 10
    @test total(Int[]) == 0
    @test total([5]) == 5
end
