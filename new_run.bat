@echo off
setlocal

REM -- musi być jeden parametr: plik wejściowy programu --
if "%~1"=="" goto usage

REM -- zapis ścieżki do pliku --
set INPUT_FILE=%1

REM -- Dodanie pustego init do katalogu z wygenerowanymi plikami ANTLR --
type nul > int\QLang\__init__.py 

REM -- Generowanie parsera ANTLR --
cd int
java -jar ..\antlr-4.13.2-complete.jar -Dlanguage=Python3 ..\QLang\QLang.g4 -o ..\int\generated -visitor 
cd ..

REM -- Wymuszenie odświeżenia cache Pythona --
set PYTHONDONTWRITEBYTECODE=1

REM -- Uruchomienie parsera i interpretera --
uv run python -m int.run %INPUT_FILE%

goto :eof

:usage
echo Sposób użycia: %0 ^<ścieżka do pliku programu>
echo Przyklad: %0 program.ql
pause