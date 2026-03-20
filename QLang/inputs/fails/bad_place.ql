obs someObs[4] = 5;
print(someObs);

// This file contains 3 places, one with its name repeated(System2 is twice)
// This should result in error

place not System1{
    print("System1");
}

place System2{
    print("System2");
}

