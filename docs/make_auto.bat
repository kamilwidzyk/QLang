cd docs
rem start the qlang highlight watcher in background
start /B uv run python -m tools.highlight
latexmk -lualatex -shell-escape -pvc -view=none -outdir=pdf -jobname=QLang -interaction=nonstopmode main.tex 
cd ..