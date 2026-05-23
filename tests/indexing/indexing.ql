text a = "1234567890";

// Negative indexing vtest
println(a[-1]);   // powinno dać: 0
println(a[-2]);   // powinno dać: 9

// Test zakresu indeksów  
text b = a[3..6];
println(b);       // powinno dać: 456

// Test listy indeksów
text c = a[[1, 4, 7]];
println(c);       // powinno dać: 258

// Test na tablicy numerycznej
num arr[5];
arr[0] = 10;
arr[1] = 20;
arr[2] = 30;
arr[3] = 40;
arr[4] = 50;

println(arr[-1]);  // powinno dać: 50
println(arr[-2]);  // powinno dać: 40

num arr2[3][3];
arr2[0][0] = 1; arr2[0][1] = 2; arr2[0][2] = 3;
arr2[1][0] = 4; arr2[1][1] = 5; arr2[1][2] = 6;
arr2[2][0] = 7; arr2[2][1] = 8; arr2[2][2] = 9;

// Testowanie dostępu do elementów dwuwymiarowej tablicy
println(arr2[1][1]);   // powinno dać: 5

// Testowanie ujemnych indeksów dwuwymiarowej tablicy
println(arr2[-1][-1]); // powinno dać: 9


// Testowanie zakresu indeksów dwuwymiarowej tablicy
num sub_arr2[2][2] = arr2[1..3][1..3];
// sub_arr2 powinno zawierać: [[5, 6], [8, 9]]
println(sub_arr2[0][0]); // powinno dać: 5

// Testowanie listy indeksów dwuwymiarowej tablicy
num list_arr2[2][2] = arr2[[0, 1]][[0, 1]];
// list_arr2 powinno zawierać: [[1, 2], [4, 5]]
println(list_arr2[0][0]); // powinno dać: 1
println(list_arr2[0][1]); // powinno dać: 2

// Testowanie mieszanych typów indeksów
num mixed_idx[3][4];
mixed_idx[0][0] = 1;
mixed_idx[-1][-1] = 3;
mixed_idx[0][2] = 2;


println(mixed_idx[0][0]); // powinno dać: 1
println(mixed_idx[-1][-1]); // powinno dać: 3
println(mixed_idx[0][2]); // powinno dać: 