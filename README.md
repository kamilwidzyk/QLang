
# Dokumentacja

Dokumentacja będzie w katalogu docs\

Wszystkie pliki mają być w katalogach, żadne pliki mają nie leżeć obok main.tex bo będzie syf

**Do kompilacji trzeba zainstalować MiKTeX i Perl**

Kompilacja do pdf: 
```    
docs\make.bat
```

Automatyczna rekompilacja po edycji plików: 
```
docs\make_auto.bat (działa jak overleaf)
```

Wynikowy PDF znajduje się w **docs/pdf/QLang.pdf**

(Polecam sobie doinstalować rozszerzenie do otwierania PDFów, żeby nie trzeba było go otwierać za każdym razem)

# Uruchomienie interpretera
```
run.bat <ścieżka do pliku QL>
```
Przykładowe pliki znajdują się w katalogu examples\

# Podświetlanie składni

Rozszerzenie do VS Code do podświetlania składni jest w:
```
highlighter\qlang\qlang<version>.vsix
```
# Uruchamianie testów
```python
Wszystkie komendy poniżej należy uruchomić w katalogu głównym projektu!!!

Uruchomienie wszystkich testów:
uv run python -m tests.test 

Uruchomienie testów w wybranym podkatalogu:
uv run python -m tests.test math\add

Uruchomienie wybranego testu:
uv run python -m tests.test <dir> <nazwa funkcji bez 'test_'>

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


