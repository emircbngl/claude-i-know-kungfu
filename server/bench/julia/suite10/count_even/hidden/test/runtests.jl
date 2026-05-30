using Test
include("../src/sol.jl")

@testset "count_even" begin
    @test count_even([1, 2, 3, 4, 6]) == 3
    @test count_even([1, 3, 5]) == 0
    @test count_even(Int[]) == 0
end
