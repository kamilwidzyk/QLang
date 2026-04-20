TODO:
✅ Dodać floaty(z notacją naukową) ✅ 
Dodać przebieg listenera za pierwszym razem
Dorobić więcej błędów składniowych

# Uruchamianie testów
```python
Wszystkie komendy poniżej należy uruchomić w katalogu głównym projektu!!!

Uruchomienie wszystkich testów:
python -m tests.test 

Uruchomienie testów w wybranym podkatalogu:
python -m tests.test math\add

Struktura pliku testowego:

from tests.test import * # import funkcji do testowania

# funkcja jest testem jeśli nazwa zaczyna się na test_
# test udany -> zwróć True
# test nieudany -> zwróć False
def test_addition() -> bool: 
    # uruchamiany plik testywy QL
    run_in_test_mode("tests\\math\\add.ql") 
    # załadowanie wszystkich linii wypisanych podczas 
    # pracy interpretera przez log_test(msg)
    # pełny log interpretera znajduje się w logs\int_out.log
    test_lines = extract_test_lines_from_log() 
    # załadowanie wszystkich wyjść z wszystkich place
    # UWAGA: W pliku QL nie wolno robić input()
    # Wszystkie logi z konsol każdego place w logs\Place <name>.log
    place_log = read_place_files_as_dict()

    if place_log.get("global") is None:
        # test nieudany(brak logu z global, coś się wysypało - pewnie syntax error)
        return False 
    
    if place_log["global"] != "4\n6\n":
        # test nieudany(wartość logu nie zgadza się z oczekiwaną)
        return False
    
    # test udany
    return True

```


# Nie patrzeć niżej
```
Teraz program uruchamia się:

.\new_run.bat <ścieżka do pliku .ql>

```

# Aktualny sposób uruchomienia programu
```
Uruchomienie tylko generowania JSON i interpretera(bez niepetrzebnych normalnie rzeczy)

.\run.bat <ścieżka do pliku .ql>

Przykłady programów znajdują się QLang\inputs
Programy, które powodują błędy są w QLang\inputs\fails

Wstępne przetworzenie programu i gramatyki do postaci dla interpretera + uruchomienie interpretera(wszystko uruchamiane z katalogu głównego):

.\parse.bat <ścieżka do pliku .ql>
uv run python -m int.main output\<nazwa pliku .ql>.json <ścieżka do pliku .ql>

np. dla pliku QLang\inputs\no_qubits.ql

.\parse.bat QLang\inputs\no_qubits.ql
uv run python -m int.main output\no_qubits.json QLang\inputs\no_qubits.ql

(jak ktoś nie ma uv to można to uruchomić bezpośrednio python -m ...)
(wygany python >= 3.14.3, jak ktoś ma jakiś błąd to sprawdzić python --version)
```



### Struktura plików:

```sql
|-- ant_out
    |-- QLang - pliki wyjściowe z ANTLR, nie ma po co tam wchodzić
|-- draw_tree
    |-- main.py - skrypt rysujący drzewo wynikowe ANTLR w SVG
|-- sim
    | <tu będą pliki związane z symulacją układu>
|-- int
    |-- QLang
        | <pliki python wygenerowane przez ANTLR>
    |-- main.py - interpreter QLang
    |-- parse.py - skrypt zapisujący drzewo w postaci JSON z numerami linii
|-- output
        Pliki wynikowe całego procesu kompilacji
        Nazwa pliku taka sama jak nazwa pliku programu QL
    |-- <name>.svg - graficzna reprezentacja drzewa
    |-- <name>.tree - tekstowa reprezentacja drzewa
    |-- <name>.json - drzewo z dopisanymi numerami linii w formacie JSON
    | <tu będzie więcej>
|-- QLang
    |-- QLang.g4 - gramatyka języka
    |-- inputs
        |-- fails
            | Pliki programów, które celowo powodują błędy podczas działania interpretera
        | Przykładowe programu w QLang
|-- antlr_gui.bat - wyświetla interaktywne drzewo parsowania, nie wyświetla się dla większych programów
|-- antlr_silent.bat - używany wewnętrznie przez parse.bat, uruchamia ANTLR
|-- antlr-4.13.2-complete.jar - ANTLR
|-- parse.bat - skrypt uruchamiający wszystko
```

### Interpreter
```
int\main.py <JSON tree> <QLang script>
```
Uruchamia interpreter na drzewie w formacie JSON z dopisanymi numerami linii dla każdego wierzchołka drzewa. Kod programu QLang będzie potrzebny do informacji do błędów(np. wyświetlenie linii i położenia błędu).

### Skrypt parse.bat
```
parse.bat plik_programu.ql
```
Skrypt będzie generował wszystkie pliki po kolei do output\ 
Na razie jest to tylko tekstowa i graficzna reprezentacja drzewa po przejściu programu przez ANTLR

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


