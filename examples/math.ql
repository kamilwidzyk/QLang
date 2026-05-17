obs base[4] = 2;
obs exp[4] = 8;
obs result[10] = base ** exp;
println();
print("Obliczenie klasyczne (2^8): ");
println(result);
print("Wynik w formacie HEX: ");
println(result, HEX);
print("Wynik w formacie BIN: ");
println(result, BIN);
if (result > 200) {
    println("Wynik jest wiekszy niz 200!");
} else {
    println("Wynik jest mniejszy lub rowny 200.");
}
println();
obs a[8] = 5;
obs b[8] = 10;
obs c[8] = 3;
obs one = 1;
obs zero = 0;
obs sum[8] = a + b;
obs diff[8] = b - a;
print("Suma (10 + 5): ");
println(sum);
print("Roznica (10 - 5): ");
println(diff);