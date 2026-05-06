place WhileExample {
    num n = 5;
    num i = 1;
    num sum = 0;

    while (i <= n) {
        sum = sum + i;
        i = i + 1;
    }

    print("Suma liczb od 1 do ");
    print(n);
    print(" wynosi: ");
    println(sum);
}
