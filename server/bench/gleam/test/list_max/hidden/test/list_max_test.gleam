import gleeunit/should
import list_max

pub fn max_test() {
  list_max.max([3, 1, 2])
  |> should.equal(3)
}

pub fn max_single_test() {
  list_max.max([5])
  |> should.equal(5)
}
