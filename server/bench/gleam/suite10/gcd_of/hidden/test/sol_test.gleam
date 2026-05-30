import gleeunit/should
import sol

pub fn gcd_basic_test() {
  sol.gcd_of(12, 18)
  |> should.equal(6)
}

pub fn gcd_b_zero_test() {
  sol.gcd_of(7, 0)
  |> should.equal(7)
}

pub fn gcd_a_zero_test() {
  sol.gcd_of(0, 5)
  |> should.equal(5)
}

pub fn gcd_coprime_test() {
  sol.gcd_of(17, 5)
  |> should.equal(1)
}
