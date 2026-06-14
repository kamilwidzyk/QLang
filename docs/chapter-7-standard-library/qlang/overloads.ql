text word = "hello world";
text clean = word - "o";       // "hell wrld"

text repeated = "ab" * 3;      // "ababab"

text path = "user/local/bin";
text parts[?] = path / "/";    // ["user", "local", "bin"]

num a[?] = [1, 2];
num b[?] = [3, 4];
num combined[?] = a + b;       // [1, 2, 3, 4]
num appended[?] = a + 5;       // [1, 2, 5]
