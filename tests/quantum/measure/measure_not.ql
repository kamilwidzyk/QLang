seed(42);

num res[2];
num iter = 100;
for i from 0 to iter{
    state x;
    not x;
    res[measure x]++;
}
println("[not] 0=%d 1=%d" % res);
