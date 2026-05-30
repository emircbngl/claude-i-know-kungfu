import gleeunit/should
import sol

pub fn largest_basic_test() {
  sol.largest([3, 1, 2])
  |> should.equal(3)
}

pub fn largest_single_test() {
  sol.largest([5])
  |> should.equal(5)
}

pub fn largest_all_equal_test() {
  sol.largest([4, 4, 4])
  |> should.equal(4)
}
