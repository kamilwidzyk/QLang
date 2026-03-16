@echo off
setlocal

REM -- utworzenie folderu output, ignorowanie błędu jeśli już istnieje -- 
mkdir output >nul 2>&1

REM -- musi być jeden parametr: plik wejściowy programu --
if "%~1"=="" goto usage

REM -- zapis ścieżki do pliku i nazwy pliku do zmiennych --
set INPUT_FILE=%1
set FILE_NAME=%~n1

REM -- Analiza programu przez ANTLR, wygenerowany zostanie plik output\nazwa.tree --
echo ANTLR: Loading and analyzing file: %INPUT_FILE% 
call .\antlr_silent.bat QLang\QLang.g4 program -f %INPUT_FILE%

REM -- Wizualizacja drzewa programu jako SVG, plik w output\nazwa.svg --
echo Visualizing parsed tree...
python draw_tree\main.py ant_out\QLang\QLang.tree output\%FILE_NAME%.svg 
copy ant_out\QLang\QLang.tree output\%FILE_NAME%.tree > nul

REM -- Wygenerowanie plików Python z ANTLR, wynik w int\QLang --
REM -- ścieżka jest ustawiona ..\int\generated, ale usunięcie tego 'generated' powoduje nadpisanie gramatyki tymi plikami, czemu to nie wiem --
echo Generating python files...
cd int
java -jar ..\antlr-4.13.2-complete.jar -Dlanguage=Python3 ..\QLang\QLang.g4 -o ..\int\generated -visitor
cd ..

REM -- Wygenerowanie drzewa programu w formacie JSON z dopisanymi liniami i pozycjami w oryginalnym programie --
echo Parsing QLang script into JSON tree...
python int\parse.py %INPUT_FILE%

REM -- Wyświetlenie lokalizacji wygenerowanych plików --
echo.
echo DONE!
echo.
echo Raw tree:      output\%FILE_NAME%.tree
echo SVG tree:      output\%FILE_NAME%.svg
echo JSON tree:     output\%FILE_NAME%.json

REM -- Tu będzie wywołanie interpretera ale jeszcze nie ---




REM -- Wyświetlenie sposobu wywołania skryptu w sytuacji niepodania odpowiednich parametrów --
goto :eof

:usage
echo Sposób użycia: %0 ^<ścieżka do pliku programu>
echo Przyklad: %0 program.ql
pause