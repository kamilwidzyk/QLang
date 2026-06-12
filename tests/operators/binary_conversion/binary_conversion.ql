obs bits[4] = [1, 0, 1, 1];
println(bits >> num); // 13
println([1, 0, 1, 1] >> num); // 13
println(13 >4> obs); // [1, 0, 1, 1]
println(0 >4> obs); // [0, 0, 0, 0]
