pub fn count_even(xs: List(Int)) -> Int {
  case xs {
    [] -> 0
    [x, ..rest] ->
      case x % 2 == 0 {
        True -> 1 + count_even(rest)
        False -> count_even(rest)
      }
  }
}
