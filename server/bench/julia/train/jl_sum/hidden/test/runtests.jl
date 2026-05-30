using Test
include("../src/jl_sum.jl")

@testset "jl_sum" begin
    @test sum_vec([1, 2, 3, 4]) == 10
    @test sum_vec(Int[]) == 0
end
