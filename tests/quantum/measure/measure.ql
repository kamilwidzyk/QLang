seed(42);

num res[2];
num iter = 100; // this will be increased after most of the logs are removed
// Measure default state -> always 0
for i from 0 to iter{
    state x;
    res[measure x]++;
}
println("[1] 0=%d 1=%d" % res); // [1] 0=100 1=0

reset res;
// Measure default state + X gate -> always 1
for i from 0 to iter{
    state x;
    X x;
    res[measure x]++;
}
println("[2] 0=%d 1=%d" % res); // [2] 0=0 1=100

reset res;
// Measure default state + NOT gate -> always 1 (the same as previous)
for i from 0 to iter{
    state x;
    not x;
    res[measure x]++;
}
println("[3] 0=%s 1=%d" % res); // [3] 0=0 1=100

reset res;
// Measure superposed(using H) state -> around 50/50

for i from 0 to iter{
    state x;
    H x;
    res[measure x]++;
}
println("[4] 0=%s 1=%d" % res); // [4] 50/50

reset res;
// Measure superposed(using superpose) state -> around 50/50

for i from 0 to iter{
    state x;
    superpose x;
    res[measure x]++;
}
println("[5] 0=%d 1=%d" % res); // [5] 50/50

// Rozkład 1/4 -> 1 i 3/4 -> 0
reset res;

for i from 0 to iter{
    state x[2];
    superpose x;
    obs x_meas[?] = measure x;
    res[x_meas == [1, 1] ? 1 : 0]++;
}

println("[6] 0=%d 1=%d" % res); // [6] 75/25

// expected output:
// 
// [1] 0=100 1=0
// [2] 0=0 1=100
// [3] 0=0 1=100
// [4] 0=56 1=44
// [5] 0=57 1=43
// [6] 0=75 1=25
//






