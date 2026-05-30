pub fn collatz(n: Int) -> Int {
  collatz_loop(n, 0)
}

fn collatz_loop(n: Int, steps: Int) -> Int {
  case n {
    1 -> steps
    _ ->
      case n % 2 == 0 {
        True -> collatz_loop(n / 2, steps + 1)
        False -> collatz_loop(3 * n + 1, steps + 1)
      }
  }
}
