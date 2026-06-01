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
}

// break and continue work inside iterate
iterate arr as val {
    if (val == 20) continue;
    if (val == 40) break;
    println(val);  // 10 30
}