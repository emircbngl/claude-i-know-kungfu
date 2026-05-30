using Test
include("../src/jl_concat.jl")

@testset "jl_concat" begin
    @test cat_str("foo", "bar") == "foobar"
    @test cat_str("", "x") == "x"
end
