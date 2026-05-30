using Test
include("../src/sol.jl")

@testset "is_prime" begin
    @test is_prime(2) == 1
    @test is_prime(7) == 1
    @test is_prime(9) == 0
    @test is_prime(1) == 0
    @test is_prime(13) == 1
end
