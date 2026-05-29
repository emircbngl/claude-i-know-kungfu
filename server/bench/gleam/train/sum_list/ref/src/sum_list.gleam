import gleam/list

pub fn sum(items: List(Int)) -> Int {
  list.fold(items, 0, fn(acc, x) { acc + x })
}
