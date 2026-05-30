pub fn fib(n: Int) -> Int {
  fib_loop(n, 0, 1)
}

fn fib_loop(n: Int, a: Int, b: Int) -> Int {
  case n {
    0 -> a
    _ -> fib_loop(n - 1, b, a + b)
  }
}
