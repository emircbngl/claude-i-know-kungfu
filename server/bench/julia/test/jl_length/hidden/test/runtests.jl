using Test
include("../src/jl_length.jl")

@testset "jl_length" begin
    @test len_vec([1, 2, 3]) == 3
    @test len_vec(Int[]) == 0
end
