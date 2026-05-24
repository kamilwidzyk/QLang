print("[A] ");
obs a;
print(a); // F
a = 0;
print(a); // F
a = 1;
println(a); // T
// [A] FFT\n

print("[B] ");
obs b = 1;
print(b); // T
b = 0;
print(b); // F
reset b;
println(b); // T
// [B] TFT\n

print("[C] ");
obs c = 0;
print(c); // F
c = 1;
print(c); // T
reset c;
println(c); // F
// [C] FTF\n

print("[DEF] ");
obs d, e, f;
print(d); // F
print(e); // F
print(f); // F
d = 1;
e = 1;
f = 1;
print(d); // T
print(e); // T
println(f); // T
// [DEF] FFFTTT\n

print("[G] ");
obs g[3] = 3;
print(g[0]); // T
print(g[1]); // T
print(g[2]); // F

g[0] = 0;
g[1] = 0;
g[2] = 0;
print(g[0]); // F
print(g[1]); // F
print(g[2]); // F

g[0] = 1;
g[1] = 1;
g[2] = 1;
print(g[0]); // T
print(g[1]); // T
println(g[2]); // T
// [G] TTFFFFTTT\n

println(g); // 7

// expected output: [A] FFT\n[B] TFT\n[C] FTF\n[DEF] FFFTTT\n[G] TTFFFFTTT\n7\n

