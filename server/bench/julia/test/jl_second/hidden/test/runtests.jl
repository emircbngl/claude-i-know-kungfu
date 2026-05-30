using Test
include("../src/jl_second.jl")

@testset "jl_second" begin
    @test second([10, 20, 30]) == 20
    @test second([1, 2]) == 2
end
