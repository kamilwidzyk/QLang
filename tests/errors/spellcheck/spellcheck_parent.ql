num parent_var = 10;
function test() {
    num local_var = ^parent_vr; // Missing 'a', triggers CFV-6
}
test();
