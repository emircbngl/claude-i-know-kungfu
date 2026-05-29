import gleeunit
import gleeunit/should
import list_reverse

pub fn main() {
  gleeunit.main()
}

pub fn reverse_test() {
  list_reverse.reverse([1, 2, 3])
  |> should.equal([3, 2, 1])
}

pub fn reverse_empty_test() {
  list_reverse.reverse([])
  |> should.equal([])
}
