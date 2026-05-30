import gleeunit/should
import sol

pub fn count_even_basic_test() {
  sol.count_even([1, 2, 3, 4, 6])
  |> should.equal(3)
}

pub fn count_even_none_test() {
  sol.count_even([1, 3, 5])
  |> should.equal(0)
}

pub fn count_even_empty_test() {
  sol.count_even([])
  |> should.equal(0)
}
