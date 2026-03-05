### Skrypt antlr.bat i antlr_gui.bat
```
antlr.bat plik_gramatyki.g4 punkt_startowy string_wejsciowy

antlr_gui.bat plik_gramatyki.g4 punkt_startowy string_wejsciowy

antlr_gui.bat plik_gramatyki.g4 punkt_startowy -f plik_wejsciowy
```
- Wymagana zainstalowana java
- Wyświetlone zostanie drzewo i zapisane do ant_out\nazwa\nazwa.tree

### Dokumentacja antlr

- [Grammar Lexicon](https://github.com/antlr/antlr4/blob/master/doc/lexicon.md)

- [Grammar Structure](https://github.com/antlr/antlr4/blob/master/doc/grammars.md)

- [Parser Rules](https://github.com/antlr/antlr4/blob/master/doc/parser-rules.md)

- [Left-recursive rules](thub.com/antlr/antlr4/blob/master/doc/left-recursion.md)



# Wymagania języka

projektowany język powinien być bezkontekstowy (ale nie regularny)


## Elementy, które powinien posiadać projektowany język:

- odpowiednik zmiennych (w tym zasięgi (scope) obowiązywania zmiennych)

- operacje arytmetyczne za zmiennych (odpowiednik dodawania, odejmowania, mnożenia, itd., nawiasowanie) 

- Typ logiczny („true”/”false”) i co najmniej podstawowe operacje logiczne (and, or, not, nawiasowanie) na zmiennych logicznych i stałych oraz porównywanie zmiennych typu numerycznego (<, > , ==, !=) co w wyniku powinno dawać typ logiczny

- rodzaj instrukcji warunkowej (odpowiednik if)

- rodzaj pętli/iteracji (odpowiednik for/while) - dowolnie zagnieżdżonych

- odpowiednik procedur/funkcji (w tym możliwość wywoływania rekurencyjnego) z z argumentami (powinna być co najmniej możliwość przekazywania argumentów przez wartość)

- 'przyjazne' dla użytkownika komunikaty o błędach. Informacja o numerze linii (i ewentualnie kolumny), w której wystąpił błąd.

- Elementy nadobowiązkowe:
translacja kodu do kodu pewnej maszyny wirtualnej. Wykonywanie kodu przez VM


