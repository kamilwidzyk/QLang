num x = 5;
println($x); // num

num lst[7];
println($lst); // list

num multi[2][3];
println($multi); // list

obs bit = 1;
println($bit); // obs

obs bytes[8] = 42 >8> obs;
println($bytes); // list


println($bytes); // list

state q;
println($q); // state

state qubits[4];
println($qubits); // list

state multi_qubits[4][2];
println($multi_qubits); // list

text s1 = "abc";
println($s1); // text

text fruits[?] = ["apple", "banana", "orange"];
println($fruits); // list

function foo(num a, num b){
    return a + b;
}

println($foo); // function

any mixed[?] = ["123", 123, 1.0];
println($mixed); // list

any mixed_list[?] = ["a", 3];
println($mixed_list[1]); // num

any any_num = 5;
println($any_num); // num

any any_text = "abc";
println($any_text); // text

// expected output:
// num\nlist\nlist\nobs\nobsRegister\nlist\nstate\nstateRegister\nlist\ntext\nlist\nfunction\nlist\nnum\ntext\n
//
//
//
//
//


