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

echo DONE!
echo Parsed tree in: output\%FILE_NAME%.tree
echo Graphical tree representation in: output\%FILE_NAME%.svg

goto :eof

:usage
echo Sposób użycia: %0 ^<ścieżka do pliku programu>
echo Przyklad: %0 program.ql
pause