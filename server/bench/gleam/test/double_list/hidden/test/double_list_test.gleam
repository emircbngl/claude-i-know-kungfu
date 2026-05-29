import gleeunit
import gleeunit/should
import double_list

pub fn main() {
  gleeunit.main()
}

pub fn double_test() {
  double_list.double([1, 2, 3])
  |> should.equal([2, 4, 6])
}

pub fn double_empty_test() {
  double_list.double([])
  |> should.equal([])
}
