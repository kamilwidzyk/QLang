<<"stdlib:math.ql">>;

num n;
print("Enter a number 0-1000: ");
input(n, 0..1000);
println("%d! = %d" % [n, factorial(n)]);