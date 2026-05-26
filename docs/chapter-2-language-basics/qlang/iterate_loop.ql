// iterate over array
num arr[4] = [10, 20, 30, 40];
iterate arr as val {
    println(val);  // 10 20 30 40
}

// iterate with index
iterate arr as val index i {
    println("%d: %d" % [i, val]);
    // 0: 10
    // 1: 20
    // 2: 30
    // 3: 40
}iterate_loop