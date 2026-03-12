@echo off
setlocal

REM -- musi być jeden parametr: plik wejściowy programu --
if "%~1"=="" goto usage

set INPUT_FILE=%1
set FILE_NAME=%~n1

echo ANTLR: Loading and analyzing file: %INPUT_FILE% 
call .\antlr_silent.bat QLang\QLang.g4 program -f %INPUT_FILE%

echo Visualizing parsed tree...

python draw_tree\main.py ant_out\QLang\QLang.tree output\%FILE_NAME%.svg 
copy ant_out\QLang\QLang.tree output\%FILE_NAME%.tree > nul

echo Generating python files...
cd int
java -jar ..\antlr-4.13.2-complete.jar -Dlanguage=Python3 ..\QLang\QLang.g4 -o ..\int\generated -visitor
cd ..

echo Parsing QLang script into JSON tree...
python int\parse.py %INPUT_FILE%

echo.
echo DONE!
echo.
echo Raw tree:      output\%FILE_NAME%.tree
echo SVG tree:      output\%FILE_NAME%.svg
echo JSON tree:     output\%FILE_NAME%.json

goto :eof

:usage
echo Sposób użycia: %0 ^<ścieżka do pliku programu>
echo Przyklad: %0 program.ql
pause