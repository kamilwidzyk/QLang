@echo off
setlocal EnableDelayedExpansion

REM ---- sprawdzanie obecności parametrów ----
if "%~2" == "" (
    echo.
    echo Blad: Nie podano wystarczajacej liczby parametrow.
    echo.
    echo Uzycie: %~nx0 ^<plik_gramatyki.g4^> ^<punkt_startowy^> [tekst do parsowania]
    echo.
    echo Przyklad: %~nx0 Kalkulator.g4 expression 2 + 2
    echo.
    echo Opis:
    echo   - plik_gramatyki.g4: Sciezka do pliku .g4
    echo   - punkt_startowy: Nazwa reguly w gramatyce, od ktorej zaczyna sie parsowanie
    echo   - tekst do parsowania: Wszystkie kolejne parametry zostana polaczone w wejscie
    exit /b 1
)

REM ---- parametry ----
set "G4FILE=%~1"
set "START_RULE=%~2"

REM Przesuwamy o dwa (plik i punkt startowy), aby reszta to byl INPUT
shift
shift

REM Zbieramy pozostałe parametry do zmiennej INPUT
set "INPUT="
:loop
if "%~1"=="" goto :continue
set "INPUT=!INPUT! %1"
shift
goto :loop

:continue
if defined INPUT set "INPUT=%INPUT:~1%"

REM ---- nazwa gramatyki bez .g4 ----
for %%F in ("%G4FILE%") do set NAME=%%~nF

REM ---- katalog wynikowy: ant_out\nazwa_pliku ----
set OUTDIR=ant_out\%NAME%

if not exist "%OUTDIR%" mkdir "%OUTDIR%"

copy "%G4FILE%" "%OUTDIR%\" >nul

pushd "%OUTDIR%"

REM ---- generowanie parsera ----
java -jar ..\..\antlr-4.13.2-complete.jar %NAME%.g4

REM ---- kompilacja ----
javac -cp ".;..\..\antlr-4.13.2-complete.jar" *.java

REM ---- zapis wejścia ----
echo %INPUT% > input.txt

REM ---- uruchomienie parsera (uzycie zmiennej %START_RULE%) ----
java -cp ".;..\..\antlr-4.13.2-complete.jar" org.antlr.v4.gui.TestRig %NAME% %START_RULE% -tree < input.txt > %NAME%.tree

echo.
echo ====== DRZEWO PARSOWANIA (Start: %START_RULE%) ======
type %NAME%.tree
echo ===============================

popd

echo.
echo Wynik zapisany w: %OUTDIR%\%NAME%.tree