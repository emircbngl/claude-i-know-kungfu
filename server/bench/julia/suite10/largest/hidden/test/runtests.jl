using Test
include("../src/sol.jl")

@testset "largest" begin
    @test largest([3, 1, 2]) == 3
    @test largest([5]) == 5
    @test largest([4, 4, 4]) == 4
end
