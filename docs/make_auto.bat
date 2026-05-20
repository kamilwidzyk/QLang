cd docs
latexmk -lualatex -pvc -view=none -outdir=pdf -jobname=QLang -interaction=nonstopmode main.tex 
cd ..