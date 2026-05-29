import gleeunit/should
import list_product

pub fn product_test() {
  list_product.product([1, 2, 3, 4])
  |> should.equal(24)
}

pub fn product_empty_test() {
  list_product.product([])
  |> should.equal(1)
}
