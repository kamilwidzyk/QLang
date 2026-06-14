num sum = 0;
for i from 1 to 3 {
    // This variable is created fresh in every iteration
    num temp = i * 10;
    sum += temp;
}
// Trying to access 'temp' or 'i' here would result in an error