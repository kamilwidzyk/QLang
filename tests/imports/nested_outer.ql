<<"tests/imports/nested_inner.ql">>;

function nested_outer() {
    return nested_inner() + 2;
}
