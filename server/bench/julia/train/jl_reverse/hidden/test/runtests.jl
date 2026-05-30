using Test
include("../src/jl_reverse.jl")

@testset "jl_reverse" begin
    @test reverse_vec([1, 2, 3]) == [3, 2, 1]
    @test reverse_vec(Int[]) == Int[]
end
