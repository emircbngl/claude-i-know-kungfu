using Test
include("../src/sol.jl")

@testset "gcd_of" begin
    @test gcd_of(12, 18) == 6
    @test gcd_of(7, 0) == 7
    @test gcd_of(0, 5) == 5
    @test gcd_of(17, 5) == 1
end
