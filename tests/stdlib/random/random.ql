<<"stdlib:random.ql">>;

seed(0);
num values[?] = random_list(list_size = 5, min_val = 0, max_val = 10, only_int = T);
println(#values);
println(values);
