import gleeunit/should
import sol

pub fn eval_precedence_test() {
  sol.eval_expr("2+3*4")
  |> should.equal(14)
}

pub fn eval_parens_test() {
  sol.eval_expr("(2+3)*4")
  |> should.equal(20)
}

pub fn eval_left_assoc_division_test() {
  sol.eval_expr("100/5/2")
  |> should.equal(10)
}

pub fn eval_subtraction_test() {
  sol.eval_expr("2+3-1")
  |> should.equal(4)
}

pub fn eval_nested_parens_test() {
  sol.eval_expr("(1+2)*(3+4)")
  |> should.equal(21)
}
