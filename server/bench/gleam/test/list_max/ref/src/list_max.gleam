import gleam/list

pub fn max(items: List(Int)) -> Int {
  list.fold(items, 0, fn(acc, x) {
    case x > acc {
      True -> x
      False -> acc
    }
  })
}
