# Error taxonomy

Every lesson is classified by the *kind* of mistake. This lets the KB show patterns
("most of this language's errors are SEMANTIC") and target retrieval. `kungfu_learn`
classifies automatically, but pass `error_type` explicitly when you know it.

| Type | What it is | Example |
| --- | --- | --- |
| `SYNTAX` | Malformed grammar | wrong block/brace/indent; `expected '}'` |
| `API-SHAPE` | Wrong signature / arity / argument order | `list.map(fn, list)` when it is `list.map(list, fn)` |
| `SEMANTIC` | Wrong mental model of how the language behaves | using `return` in an expression-oriented language |
| `NONEXISTENT` | Hallucinated a symbol/feature that does not exist | calling `list.fold_left` when only `list.fold` exists |
| `DEPENDENCY` | Wrong import / missing module / package mismatch | importing `gleam/listx`; missing dep in manifest |
| `VERSION-DRIFT` | Was right once, changed across versions | an API removed/renamed in a newer release |
| `IDIOM` | Compiles, but not the idiomatic / safe way | manual recursion where a stdlib combinator exists |

`NONEXISTENT` and `SEMANTIC` are the two that matter most for unknown languages —
they are where confident pattern-matching produces plausible, wrong code. Negative
knowledge (in the skeleton) is the direct counter to `NONEXISTENT`.
