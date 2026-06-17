function greetUser(num count) {
   println("--- Rozpoczynam powitanie ---");
   for i from 1 to count+1 {
      println("Wiadomosc nr %d: Hello, QLang World!" % i);
   }
   println("--- Koniec powitania ---");
}

num repeatTimes;
print("Podaj liczbe 1-10: ");
input(repeatTimes, 1..10);
greetUser(repeatTimes);