import gleam/list

pub fn double(items: List(Int)) -> List(Int) {
  list.map(items, fn(x) { x * 2 })
}
