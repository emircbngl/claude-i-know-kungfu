import gleam/int
import gleam/string

pub type Token {
  Num(Int)
  Op(String)
}

pub fn eval_expr(s: String) -> Int {
  let tokens = tokenize(string.to_graphemes(s), [])
  let #(value, _rest) = parse_expr(tokens)
  value
}

fn tokenize(chars: List(String), acc: List(Token)) -> List(Token) {
  case chars {
    [] -> list_reverse(acc, [])
    [c, ..rest] ->
      case is_digit(c) {
        True -> {
          let #(num, remaining) = lex_number(rest, c)
          tokenize(remaining, [Num(num), ..acc])
        }
        False -> tokenize(rest, [Op(c), ..acc])
      }
  }
}

fn lex_number(chars: List(String), seen: String) -> #(Int, List(String)) {
  case chars {
    [c, ..rest] ->
      case is_digit(c) {
        True -> lex_number(rest, string.append(seen, c))
        False -> #(to_int(seen), chars)
      }
    [] -> #(to_int(seen), [])
  }
}

fn is_digit(c: String) -> Bool {
  case c {
    "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" -> True
    _ -> False
  }
}

fn to_int(s: String) -> Int {
  case int.parse(s) {
    Ok(n) -> n
    Error(_) -> 0
  }
}

fn parse_expr(tokens: List(Token)) -> #(Int, List(Token)) {
  let #(left, rest) = parse_term(tokens)
  parse_expr_rest(left, rest)
}

fn parse_expr_rest(acc: Int, tokens: List(Token)) -> #(Int, List(Token)) {
  case tokens {
    [Op("+"), ..rest] -> {
      let #(right, remaining) = parse_term(rest)
      parse_expr_rest(acc + right, remaining)
    }
    [Op("-"), ..rest] -> {
      let #(right, remaining) = parse_term(rest)
      parse_expr_rest(acc - right, remaining)
    }
    _ -> #(acc, tokens)
  }
}

fn parse_term(tokens: List(Token)) -> #(Int, List(Token)) {
  let #(left, rest) = parse_factor(tokens)
  parse_term_rest(left, rest)
}

fn parse_term_rest(acc: Int, tokens: List(Token)) -> #(Int, List(Token)) {
  case tokens {
    [Op("*"), ..rest] -> {
      let #(right, remaining) = parse_factor(rest)
      parse_term_rest(acc * right, remaining)
    }
    [Op("/"), ..rest] -> {
      let #(right, remaining) = parse_factor(rest)
      parse_term_rest(acc / right, remaining)
    }
    _ -> #(acc, tokens)
  }
}

fn parse_factor(tokens: List(Token)) -> #(Int, List(Token)) {
  case tokens {
    [Num(n), ..rest] -> #(n, rest)
    [Op("("), ..rest] -> {
      let #(value, remaining) = parse_expr(rest)
      case remaining {
        [Op(")"), ..after] -> #(value, after)
        _ -> #(value, remaining)
      }
    }
    _ -> #(0, tokens)
  }
}

fn list_reverse(items: List(a), acc: List(a)) -> List(a) {
  case items {
    [] -> acc
    [x, ..rest] -> list_reverse(rest, [x, ..acc])
  }
}
