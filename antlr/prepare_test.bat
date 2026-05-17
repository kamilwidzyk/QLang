@echo off
setlocal

REM -- Dodanie pustego init do katalogu z wygenerowanymi plikami ANTLR --
type nul > int\QLang\__init__.py 

REM -- Generowanie parsera ANTLR --
cd antlr
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 QLang.g4 -o ..\int\QLang\ -visitor 
cd ..