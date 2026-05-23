seed(42);

num res[2];
num iter = 100;
for i from 0 to iter{
    state x;
    Z x;
    res[measure x]++;
}
println("[Z] 0=%d 1=%d" % res);
