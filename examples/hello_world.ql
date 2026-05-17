place ClassicalSystem {
   function greetUser(obs count[8]) {
   println("--- Rozpoczynam powitanie ---");
   
      for i from 1 to count {
         print("Wiadomosc nr ");
         print(i);
         print(": ");
         println("Hello, QLang World!");
   }
   
      println("--- Koniec powitania ---");
   }

   obs repeatTimes[8];
   print("Podaj liczbe 1-10: ");
   input(repeatTimes);
   println(greetUser(repeatTimes));
}