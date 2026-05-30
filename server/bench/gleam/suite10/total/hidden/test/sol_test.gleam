import gleeunit/should
import sol

pub fn total_basic_test() {
  sol.total([1, 2, 3, 4])
  |> should.equal(10)
}

pub fn total_empty_test() {
  sol.total([])
  |> should.equal(0)
}

pub fn total_single_test() {
  sol.total([5])
  |> should.equal(5)
}
