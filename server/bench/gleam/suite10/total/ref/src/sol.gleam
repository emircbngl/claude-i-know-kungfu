pub fn total(xs: List(Int)) -> Int {
  case xs {
    [] -> 0
    [x, ..rest] -> x + total(rest)
  }
}
