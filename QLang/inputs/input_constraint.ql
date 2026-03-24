obs a[8];
obs b[8];
obs c[8];
print("Maximum: ");
input(a);
print("Minimum: ");
input(b);

print("Now you can test the max and min(min..max): ");
input(c, b..a);
print("c is "); 
println(c);

print("The range way: ");
input(c, range(b, a));
print("c is ");
println(c);
