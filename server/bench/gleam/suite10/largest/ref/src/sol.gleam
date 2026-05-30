pub fn largest(xs: List(Int)) -> Int {
  case xs {
    [] -> 0
    [x] -> x
    [x, ..rest] -> {
      let m = largest(rest)
      case x > m {
        True -> x
        False -> m
      }
    }
  }
}
