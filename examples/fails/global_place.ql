obs someObs[4] = 5;
print(someObs);

// Trying to create a place named 'global'
// This should result in error

place System1{
    print("System1");
}

place global{ // <- place cannot be named 'global'
    print("Global place");
}

