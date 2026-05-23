seed(42);

num res[2];
num iter = 100;
for i from 0 to iter{
    state a;
    state b;
    H a;
    H b;
    CZ a -> b;
    res[measure a == measure b ? 0 : 1]++;
}
println("[CZ] 0=%d 1=%d" % res);
