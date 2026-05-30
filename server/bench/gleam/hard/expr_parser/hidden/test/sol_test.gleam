import gleeunit/should
import sol

pub fn precedence_test() {
  sol.eval("2+3*4")
  |> should.equal(14)
}

pub fn parens_test() {
  sol.eval("(2+3)*4")
  |> should.equal(20)
}

pub fn left_assoc_division_test() {
  sol.eval("100/5/2")
  |> should.equal(10)
}

pub fn nested_parens_test() {
  sol.eval("(1+2)*(3+4)")
  |> should.equal(21)
}

pub fn subtraction_test() {
  sol.eval("2+3-1")
  |> should.equal(4)
}
