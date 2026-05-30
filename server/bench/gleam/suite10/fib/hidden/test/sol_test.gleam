import gleeunit/should
import sol

pub fn fib_zero_test() {
  sol.fib(0)
  |> should.equal(0)
}

pub fn fib_one_test() {
  sol.fib(1)
  |> should.equal(1)
}

pub fn fib_ten_test() {
  sol.fib(10)
  |> should.equal(55)
}

pub fn fib_twenty_test() {
  sol.fib(20)
  |> should.equal(6765)
}
