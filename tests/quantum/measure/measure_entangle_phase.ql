seed(42);

num res[2];
num iter = 100;
for i from 0 to iter{
    state a;
    state b;
    H a;
    H b;
    entangle_phase a -> b;
    res[measure a == measure b ? 0 : 1]++;
}
println("[entangle_phase] 0=%d 1=%d" % res);
