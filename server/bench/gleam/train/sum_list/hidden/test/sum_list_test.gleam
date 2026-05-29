import gleeunit
import gleeunit/should
import sum_list

pub fn main() {
  gleeunit.main()
}

pub fn sum_test() {
  sum_list.sum([1, 2, 3, 4])
  |> should.equal(10)
}

pub fn sum_empty_test() {
  sum_list.sum([])
  |> should.equal(0)
}
