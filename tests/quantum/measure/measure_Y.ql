seed(42);

num res[2];
num iter = 100;
for i from 0 to iter{
    state x;
    Y x;
    res[measure x]++;
}
println("[Y] 0=%d 1=%d" % res);
