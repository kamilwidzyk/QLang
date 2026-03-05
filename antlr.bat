@echo off
setlocal EnableDelayedExpansion

REM ---- sprawdzanie obecności parametrów ----
if "%~1"=="" (
    echo.
    echo Blad: Nie podano pliku gramatyki.
    echo.
    echo Uzycie: %~nx0 plik_gramatyki.g4 [tekst do parsowania]
    echo.
    echo Przyklad: %~nx0 MojaGramatyka.g4 1 + 2 * 3
    echo.
    echo Skrypt wygeneruje parser, skompiluje go i zapisze drzewo 
    echo parsowania w katalogu ant_out\MojaGramatyka
    exit /b 1
)

REM ---- parametry ----
set G4FILE=%1
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

REM ---- generowanie parsera (..\..\ bo wychodzimy z ant_out\nazwa) ----
java -jar ..\..\antlr-4.13.2-complete.jar %NAME%.g4

REM ---- kompilacja ----
javac -cp ".;..\..\antlr-4.13.2-complete.jar" *.java

REM ---- zapis wejścia ----
echo %INPUT% > input.txt

REM ---- uruchomienie parsera ----
java -cp ".;..\..\antlr-4.13.2-complete.jar" org.antlr.v4.gui.TestRig %NAME% r -tree < input.txt > %NAME%.tree

echo.
echo ====== DRZEWO PARSOWANIA ======
type %NAME%.tree
echo ===============================

popd

echo.
echo Wynik zapisany w: %OUTDIR%\%NAME%.tree