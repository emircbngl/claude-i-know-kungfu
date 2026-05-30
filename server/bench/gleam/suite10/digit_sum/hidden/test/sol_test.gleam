import gleeunit/should
import sol

pub fn digit_sum_basic_test() {
  sol.digit_sum(1234)
  |> should.equal(10)
}

pub fn digit_sum_zero_test() {
  sol.digit_sum(0)
  |> should.equal(0)
}

pub fn digit_sum_repeated_test() {
  sol.digit_sum(99)
  |> should.equal(18)
}
