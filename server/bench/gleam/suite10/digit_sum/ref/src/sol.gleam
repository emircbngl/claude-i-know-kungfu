pub fn digit_sum(n: Int) -> Int {
  case n {
    0 -> 0
    _ -> n % 10 + digit_sum(n / 10)
  }
}
