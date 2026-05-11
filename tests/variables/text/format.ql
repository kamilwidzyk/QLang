text x = "test %d %s" % [42, "value"];
println(x); // test 42 value

text y = "test %d %s";
y %= [42, "value"];
println(y); // test 42 value