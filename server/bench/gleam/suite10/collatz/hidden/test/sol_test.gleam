import gleeunit/should
import sol

pub fn collatz_one_test() {
  sol.collatz(1)
  |> should.equal(0)
}

pub fn collatz_six_test() {
  sol.collatz(6)
  |> should.equal(8)
}

pub fn collatz_twentyseven_test() {
  sol.collatz(27)
  |> should.equal(111)
}
