using Test
include("../src/sol.jl")

@testset "bigint_factorial" begin
    @test fact(5) == 120
    @test fact(0) == 1
    # 25! overflows Int64; this only passes with BigInt arithmetic.
    @test fact(25) == parse(BigInt, "15511210043330985984000000")
end
