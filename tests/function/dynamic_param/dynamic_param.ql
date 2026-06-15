function sum_array(num a[?]) {
    num i = 0;
    num total = 0;
    for i from 0 to #a {
        total += a[i];
    }
    return total;
}

num array[?] = [1, 2, 3, 4];
num result = sum_array(array);
println(result);
