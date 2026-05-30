pub fn is_prime(n: Int) -> Int {
  case n < 2 {
    True -> 0
    False -> check_divisors(n, 2)
  }
}

fn check_divisors(n: Int, d: Int) -> Int {
  case d * d > n {
    True -> 1
    False ->
      case n % d == 0 {
        True -> 0
        False -> check_divisors(n, d + 1)
      }
  }
}
