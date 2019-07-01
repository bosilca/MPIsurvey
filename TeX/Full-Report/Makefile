TARGET = mpi-survey-full
TSRC    = $(TARGET).tex
BIBS   = ../ref.bib 
LATEX  = xelatex

CSV    = ../csv/MPI\ International\ Survey.csv
PROGDIR = ../..
PROG   = $(PROGDIR)/analyze.py
PSRC    = $(PROG).in
OPTS_ALL = -t -s all -c all
OPTS_TEX = -x -O ../inputs 
OPTS_PDF =  -o ../pdfs -f pdf
OPTS_PNG =  -o ../pngs -f png
OPTS   =  $(OPTS_ALL) $(OPTS_PDF) $(OPTS_TEX) $(INPUT)
TEMPLATES = SIMPLE.template OTHER.template CROSS.template

PDF    = $(TARGET).pdf

# directories

all : $(PDF)

$(PROG) : $(PSRC)
	cd $(PROGDIR) ; ./build.sh

python : $(PROG)

tex : $(PROG)
	$(PROG) $(OPTS_ALL) $(OPTS_TEX) $(CSV)

graphs : $(PROG)
	$(PROG) $(OPTS_ALL) $(OPTS_PDF) $(CSV)

pngs : $(PROG)
	$(PROG) $(OPTS_ALL) $(OPTS_PNG) $(CSV)

debug :  $(PROG)
	$(PROG) $(OPTS_ALL) $(OPTS_PDF) --DEBUG $(CSV)

OUTPUT = ../inputs/Q1-ans.tex

$(OUTPUT) : $(PROG) $(CSV)
	$(PROG) $(OPTS) $(CSV)

TEMPLATE = ../inputs/Q1.tex

$(TEMPLATE) : $(TEMPLATES)
	./template.sh

templates : $(TEMPLATE)

$(PDF) : $(TEMPLATE) $(TSRC) $(BIBS) $(PROG) $(OUTPUT) Makefile
	$(LATEX) $(TARGET);		\
	bibtex $(TARGET);		\
	$(LATEX) $(TARGET);		\
	$(LATEX) $(TARGET);		\
	grep -e $(LATEX) -e "LaTeX\ Warning" -e "Package\ natbib\ Warning" -e "undefined" -e "multiply\ defined" $(TARGET).log;	\

clean:
	rm -f $(PDF) *.bbl *.blg *.out *.aux *.log *~ *.dvi

veryclean: clean
	rm -f $(PROG) $(PDF) ../inputs/Q*.tex ../figs/Q*.pdf *.tex.org

PDF    = $(TARGET).pdf
