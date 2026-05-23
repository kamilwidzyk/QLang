seed(42);

num res[2];
num iter = 100;
for i from 0 to iter{
    state a;
    state b;
    H a;
    CNOT a -> b;
    res[measure a == measure b ? 0 : 1]++;
}
println("[CNOT] 0=%d 1=%d" % res);
