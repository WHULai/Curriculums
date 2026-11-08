#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p tmp/build
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=tmp/build main.tex
cp tmp/build/main.pdf main.pdf
