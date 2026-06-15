num numbers[?] = [10, 20, 30, 40, 50];

iterate numbers as n {
    println(n);
} // 10\n20\n30\n40\n50\n

iterate numbers as n index i{
    println("%d: %d" % [i, n]);
} // 0: 10\n1: 20\n2: 30\n3: 40\n4: 50\n

text fruits[?] = ["apple", "banana", "cherry"];
iterate fruits as fruit{
    println(fruit);
} // apple\nbanana\ncherry\n

function returnMixedList(){
    return ["text", 123, [1, "b"]];
}

iterate returnMixedList() as elem {
    println(elem);
} // text\n123\n[1, "b"]\n

iterate [["a", "bb"], ["c"], 42, "pi"] as x {
    println(x);
    println("size %d" % [#x]);
    println("type %s" % [$x]);
} // ["a", "bb"]\nsize 2\ntype list\n["c"]\nsize 1\ntype list\n42\nsize 1\ntype num\npi\nsize 2\ntype text\n

iterate [1, 2, 3] as x {
    println(x); 
} // 1\n2\n3\n

iterate [1, 2, 3] as x {
    if (x == 1) continue;
    if (x == 2) break;
    println(x);
}

println("Done iterating"); // Done iterating\n

// expected output: 10\n20\n30\n40\n50\n0: 10\n1: 20\n2: 30\n3: 40\n4: 50\napple\nbanana\ncherry\ntext\n123\n[1, "b"]\n["a", "bb"]\nsize 2\ntype list\n["c"]\nsize 1\ntype list\n42\nsize 1\ntype num\npi\nsize 2\ntype text\n1\n2\n3\nDone iterating\n
