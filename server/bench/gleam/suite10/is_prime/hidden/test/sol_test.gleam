import gleeunit/should
import sol

pub fn is_prime_two_test() {
  sol.is_prime(2)
  |> should.equal(1)
}

pub fn is_prime_seven_test() {
  sol.is_prime(7)
  |> should.equal(1)
}

pub fn is_prime_nine_test() {
  sol.is_prime(9)
  |> should.equal(0)
}

pub fn is_prime_one_test() {
  sol.is_prime(1)
  |> should.equal(0)
}

pub fn is_prime_thirteen_test() {
  sol.is_prime(13)
  |> should.equal(1)
}
