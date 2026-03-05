@echo off
setlocal EnableDelayedExpansion

REM ---- sprawdzanie obecności parametrów ----
if "%~2" == "" (
    echo.
    echo Blad: Nie podano wystarczajacej liczby parametrow.
    echo.
    echo Uzycie: %~nx0 ^<plik_gramatyki.g4^> ^<punkt_startowy^> ^<tekst LUB -f plik_wejsciowy^>
    echo.
    echo Przyklady:
    echo   1. %~nx0 Logo.g4 prog fd 100 rt 90
    echo   2. %~nx0 Logo.g4 prog -f moje_polecenia.txt
    exit /b 1
)

set "G4FILE=%~1"
set "START_RULE=%~2"
set "FILE_MODE=0"

REM Sprawdzenie czy trzeci parametr to flaga pliku
if "%~3" == "-f" (
    set "FILE_MODE=1"
    set "DATA_SOURCE=%~4"
    if not exist "!DATA_SOURCE!" (
        echo Blad: Plik wejsciowy "!DATA_SOURCE!" nie istnieje.
        exit /b 1
    )
)

REM ---- Przygotowanie nazwy i folderu ----
for %%F in ("%G4FILE%") do set NAME=%%~nF
set OUTDIR=ant_out\%NAME%
if not exist "%OUTDIR%" mkdir "%OUTDIR%"
copy "%G4FILE%" "%OUTDIR%\" >nul

REM ---- Logika wczytywania wejścia ----
if "!FILE_MODE!" == "1" (
    copy "!DATA_SOURCE!" "%OUTDIR%\input.txt" >nul
    echo Wczytano dane z pliku: !DATA_SOURCE!
) else (
    REM Przesuwamy o dwa, aby reszta to byl INPUT tekstowy
    shift
    shift
    set "INPUT="
    :loop
    if "%~1"=="" goto :continue
    set "INPUT=!INPUT! %1"
    shift
    goto :loop
    :continue
    if defined INPUT set "INPUT=%INPUT:~1%"
    echo !INPUT! > "%OUTDIR%\input.txt"
)

pushd "%OUTDIR%"

REM ---- generowanie i kompilacja ----
java -jar ..\..\antlr-4.13.2-complete.jar %NAME%.g4
javac -cp ".;..\..\antlr-4.13.2-complete.jar" *.java

REM ---- 1. Drzewo tekstowe ----
type input.txt | java -cp ".;..\..\antlr-4.13.2-complete.jar" org.antlr.v4.gui.TestRig %NAME% %START_RULE% -tree > %NAME%.tree

echo.
echo ====== DRZEWO PARSOWANIA (Tekst) ======
type %NAME%.tree
echo.

REM ---- 2. GUI (przez cmd /c dla kompatybilnosci z PowerShell) ----
echo Otwieranie podgladu graficznego...
start "ANTLR GUI" cmd /c "type input.txt | java -cp ".;..\..\antlr-4.13.2-complete.jar" org.antlr.v4.gui.TestRig %NAME% %START_RULE% -gui"

popd