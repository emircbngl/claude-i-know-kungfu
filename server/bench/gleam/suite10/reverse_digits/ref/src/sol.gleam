pub fn reverse_digits(n: Int) -> Int {
  reverse_loop(n, 0)
}

fn reverse_loop(n: Int, acc: Int) -> Int {
  case n {
    0 -> acc
    _ -> reverse_loop(n / 10, acc * 10 + n % 10)
  }
}
