@echo off
setlocal

REM -- zapis ścieżki do pliku --
set INPUT_FILE=%1

REM -- Wymuszenie odświeżenia cache Pythona --
set PYTHONDONTWRITEBYTECODE=1

REM -- Uruchomienie parsera i interpretera --
uv run python -m int.run %INPUT_FILE% TEST_MODE > logs\int_out.log 2>&1
