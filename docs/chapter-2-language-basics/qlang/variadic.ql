function sum(...values) {
    obs total[32] = 0;
    for i from 0 to #values {
        total += values[i];
    }
    return total;
}

println(sum(1, 2, 3, 4, 5));   // 15
