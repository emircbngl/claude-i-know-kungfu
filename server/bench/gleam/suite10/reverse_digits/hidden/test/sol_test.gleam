import gleeunit/should
import sol

pub fn reverse_basic_test() {
  sol.reverse_digits(1230)
  |> should.equal(321)
}

pub fn reverse_single_test() {
  sol.reverse_digits(7)
  |> should.equal(7)
}

pub fn reverse_trailing_zeros_test() {
  sol.reverse_digits(100)
  |> should.equal(1)
}

pub fn reverse_zero_test() {
  sol.reverse_digits(0)
  |> should.equal(0)
}
