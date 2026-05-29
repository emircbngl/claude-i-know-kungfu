import gleeunit
import gleeunit/should
import list_length

pub fn main() {
  gleeunit.main()
}

pub fn count_test() {
  list_length.count([1, 2, 3])
  |> should.equal(3)
}

pub fn count_empty_test() {
  list_length.count([])
  |> should.equal(0)
}
