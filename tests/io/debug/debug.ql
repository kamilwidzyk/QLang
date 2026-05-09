num x = 42;
debug(x);
num y = 3.14;
debug(y);

num z[3] = [1, 2, 3];
debug(z);
debug(z[1]);

obs a = 0;
debug(a);

obs b[5] = 5;
debug(b);

num c[3][3][3];
debug(c);
debug(c[2]);

num d[3][3] = c[2];
debug(d);

function f1(num x, num y[5]){}
debug(f1);
