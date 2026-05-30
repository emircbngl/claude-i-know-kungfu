# Reference: recursive-descent evaluator for integer arithmetic expressions.
#
# Grammar (precedence climbing by hand):
#   expr   := term (('+' | '-') term)*       # lowest precedence, left-assoc
#   term   := factor (('*' | '/') factor)*   # higher precedence, left-assoc
#   factor := number | '(' expr ')'
#
# '/' is INTEGER division via div(...), and every intermediate value is an Int,
# so the result is an Int (Julia's `/` would otherwise return a Float64).

function eval_expr(s::AbstractString)
    chars = [c for c in s if !isspace(c)]
    pos = Ref(1)
    n = length(chars)

    peek() = pos[] <= n ? chars[pos[]] : '\0'
    advance() = (pos[] += 1)

    function parse_factor()
        if peek() == '('
            advance()                  # consume '('
            v = parse_expr()
            advance()                  # consume ')'
            return v
        end
        # read a (multi-digit) non-negative integer literal
        val = 0
        while pos[] <= n && isdigit(peek())
            val = val * 10 + (Int(peek()) - Int('0'))
            advance()
        end
        return val
    end

    function parse_term()
        v = parse_factor()
        while peek() == '*' || peek() == '/'
            op = peek()
            advance()
            rhs = parse_factor()
            v = op == '*' ? v * rhs : div(v, rhs)
        end
        return v
    end

    function parse_expr()
        v = parse_term()
        while peek() == '+' || peek() == '-'
            op = peek()
            advance()
            rhs = parse_term()
            v = op == '+' ? v + rhs : v - rhs
        end
        return v
    end

    return parse_expr()
end
