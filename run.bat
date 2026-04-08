@echo off
setlocal

REM -- utworzenie folderu output, ignorowanie błędu jeśli już istnieje -- 
mkdir output >nul 2>&1

REM -- musi być jeden parametr: plik wejściowy programu --
if "%~1"=="" goto usage

REM -- zapis ścieżki do pliku i nazwy pliku do zmiennych --
set INPUT_FILE=%1
set FILE_NAME=%~n1
set ERROR_FILE=output\%FILE_NAME%.error

REM -- usuń poprzedni plik błędu jeśli istnieje --
if exist "%ERROR_FILE%" del "%ERROR_FILE%"

echo Parsing...

REM -- Generowanie parsera ANTLR + przechwycenie błędów --
cd int
java -jar ..\antlr-4.13.2-complete.jar -Dlanguage=Python3 ..\QLang\QLang.g4 -o ..\int\generated -visitor 2> ..\%ERROR_FILE%
cd ..

REM -- jeśli plik pusty → usuń --
if exist "%ERROR_FILE%" (
    for %%A in ("%ERROR_FILE%") do if %%~zA==0 del "%ERROR_FILE%"
)

REM -- Parsowanie do JSON (bez przechwytywania błędów) --
python int\parse.py %INPUT_FILE%

echo DONE!

REM -- Wywołanie interpretera --
if exist "%ERROR_FILE%" (
    echo Errors detected, passing ANTLR error file...
    uv run python -m int.main output\%FILE_NAME%.json %INPUT_FILE% %ERROR_FILE%
) else (
    uv run python -m int.main output\%FILE_NAME%.json %INPUT_FILE%
)

goto :eof

:usage
echo Sposób użycia: %0 ^<ścieżka do pliku programu>
echo Przyklad: %0 program.ql
pause