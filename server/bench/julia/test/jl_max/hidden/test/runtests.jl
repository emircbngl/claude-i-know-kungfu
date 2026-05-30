using Test
include("../src/jl_max.jl")

@testset "jl_max" begin
    @test max_vec([3, 1, 2]) == 3
    @test max_vec([5]) == 5
end
