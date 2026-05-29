import gleam/list

pub fn product(items: List(Int)) -> Int {
  list.fold(items, 1, fn(acc, x) { acc * x })
}
