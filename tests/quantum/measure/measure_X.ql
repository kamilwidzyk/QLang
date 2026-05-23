seed(42);

num res[2];
num iter = 100;
for i from 0 to iter{
    state x;
    X x;
    res[measure x]++;
}
println("[X] 0=%d 1=%d" % res);
