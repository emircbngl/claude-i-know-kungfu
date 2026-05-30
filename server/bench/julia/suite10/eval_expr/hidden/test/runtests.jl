using Test
include("../src/sol.jl")

@testset "eval_expr" begin
    @test eval_expr("2+3*4") == 14
    @test eval_expr("(2+3)*4") == 20
    @test eval_expr("100/5/2") == 10
    @test eval_expr("2+3-1") == 4
    @test eval_expr("(1+2)*(3+4)") == 21
end
