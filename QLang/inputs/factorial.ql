place calculatingFactorial {
    function factorial(obs n[32]) {
        if (n < 0){
            return 0;
        }
        if (n == 0){
            return 1;
        }
        return n*factorial(n-1);
    }
    
    obs num[32];
    print("Podaj liczbę -> ");
    input(num);
    print(factorial(num));
}