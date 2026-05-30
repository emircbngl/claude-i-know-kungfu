pub fn gcd_of(a: Int, b: Int) -> Int {
  case b {
    0 -> a
    _ -> gcd_of(b, a % b)
  }
}
