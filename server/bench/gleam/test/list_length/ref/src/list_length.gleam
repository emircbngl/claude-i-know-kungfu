import gleam/list

pub fn count(items: List(a)) -> Int {
  list.length(items)
}
