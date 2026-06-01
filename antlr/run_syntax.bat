@echo off
setlocal

REM -- zapis ścieżki do pliku --
set INPUT_FILE=%1

REM -- Wymuszenie odświeżenia cache Pythona --
set PYTHONDONTWRITEBYTECODE=1

REM -- Dodanie folderu logs jeśli go nie ma --
if not exist logs mkdir logs

REM -- Uruchomienie parsera i interpretera --
uv run python -m int.run %INPUT_FILE% SYNTAX_MODE > logs\int_out.log 2>&1
