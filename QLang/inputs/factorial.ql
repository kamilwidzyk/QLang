place calculatingFactorial {
    function factorial(obs n[32]) {
        if (n == 0){
            return 1;
        }
        return n*factorial(n-1);
    }
    
    obs numb[32];
    print("Enter a number 0-1000: ");
    input(numb, 0 ..1000);
    
    print(numb);
    print("! = ");
    println(factorial(numb));
}