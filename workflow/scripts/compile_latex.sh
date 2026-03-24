#!/bin/bash
# compile_latex.sh — Full LaTeX compilation cycle for JAMA papers
#
# Usage: bash compile_latex.sh paper.tex
#        bash compile_latex.sh /path/to/paper.tex
#
# Runs pdflatex + bibtex + pdflatex x2 to resolve all references.
# Exits with 0 on success, 1 on failure.

set -e

if [ -z "$1" ]; then
    echo "Usage: bash compile_latex.sh <texfile>"
    echo "Example: bash compile_latex.sh paper.tex"
    exit 1
fi

TEXFILE="$1"
TEXDIR="$(cd "$(dirname "$TEXFILE")" && pwd)"
BASENAME="$(basename "$TEXFILE" .tex)"

cd "$TEXDIR"

echo "=== Compiling $BASENAME.tex in $TEXDIR ==="
echo ""

echo "--- Pass 1: pdflatex (initial compilation) ---"
pdflatex -interaction=nonstopmode "$BASENAME.tex" > /dev/null 2>&1 || true

echo "--- Pass 2: bibtex (resolve references) ---"
bibtex "$BASENAME" > /dev/null 2>&1 || true

echo "--- Pass 3: pdflatex (incorporate references) ---"
pdflatex -interaction=nonstopmode "$BASENAME.tex" > /dev/null 2>&1 || true

echo "--- Pass 4: pdflatex (resolve cross-references) ---"
pdflatex -interaction=nonstopmode "$BASENAME.tex" > /dev/null 2>&1 || true

if [ -f "$BASENAME.pdf" ]; then
    PAGES=$(pdfinfo "$BASENAME.pdf" 2>/dev/null | grep "Pages:" | awk '{print $2}' || echo "unknown")
    SIZE=$(du -h "$BASENAME.pdf" | cut -f1)
    echo ""
    echo "=== SUCCESS ==="
    echo "Output: $TEXDIR/$BASENAME.pdf"
    echo "Size: $SIZE"
    echo "Pages: $PAGES"
    exit 0
else
    echo ""
    echo "=== FAILED ==="
    echo "PDF was not generated. Check $BASENAME.log for errors."
    echo ""
    echo "--- Last 30 lines of log ---"
    tail -30 "$BASENAME.log" 2>/dev/null || echo "(no log file found)"
    exit 1
fi
