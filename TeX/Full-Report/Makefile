TARGET = mpi-survey-full
TSRC    = $(TARGET).tex
BIBS   = ../ref.bib 
LATEX  = xelatex

CSVS    = ../csv/MPI\ International\ Survey.csv ../csv/MPI\ International\ Survey-Microsoft.csv
PROGDIR = ../..
TEMPDIR = ../templates
PROG   = $(PROGDIR)/analyze.py
OPTS_ALL = -t -s all -c all -V ../dat
OPTS_TEX = -x -O ../inputs 
OPTS_PDF =  -o ../pdfs -f pdf
OPTS_PNG =  -o ../pngs -f png
OPTS   =  $(OPTS_ALL) $(OPTS_PDF) $(OPTS_TEX) $(INPUT)
TMPDIR = ../templates
TEMPLATE = $(TMPDIR)/Q1.tex
TEMPLATES = $(TMPDIR)/SIMPLE.template \
	$(TMPDIR)/OTHER.template \
	$(TMPDIR)/CROSS.template
CHAPS = $(shell ls chaps/*.tex)
DISCUSS = $(shell ls discuss/*.tex)

PDF    = $(TARGET).pdf

# directories

all: $(PDF) Makefile

python: $(PROG)

tex: $(PROG)
	$(PROG) $(OPTS_ALL) $(OPTS_TEX) $(CSVS)

graphs: $(PROG)
	$(PROG) $(OPTS_ALL) $(OPTS_PDF) $(CSVS)

pngs: $(PROG)
	$(PROG) $(OPTS_ALL) $(OPTS_PNG) $(CSVS)

debug:  $(PROG)
	$(PROG) $(OPTS_ALL) $(OPTS_PDF) --DEBUG $(CSVS)

OUTPUT = ../inputs/Q1-ans.tex

$(OUTPUT): $(PROG) $(CSVS)
	$(PROG) $(OPTS) $(CSVS)

$(TEMPLATE): $(TEMPLATES)
	./template.sh

$(PDF): $(CHAPS) $(DISCUSS) $(TEMPLATE) $(TSRC) $(BIBS) $(PROG) $(OUTPUT) $(CSVS) questionnaire.tex Makefile
	$(LATEX) $(TARGET);
	bibtex $(TARGET);
	$(LATEX) $(TARGET);
	$(LATEX) $(TARGET);
	grep -e $(LATEX) -e "LaTeX\ Warning" -e "Package\ natbib\ Warning" -e "undefined" -e "multiply\ defined" $(TARGET).log;

clean:
	rm -f $(PDF) *.bbl *.blg *.out *.aux *.toc *.tdo *.log *~ *.dvi

veryclean: clean
	rm -f $(PDF) ../inputs/Q*.tex ../pdfs/Q*.pdf \
	../templates/*.tex ../templates/*.tex*

PDF    = $(TARGET).pdf
