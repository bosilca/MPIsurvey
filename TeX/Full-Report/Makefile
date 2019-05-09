TARGET = mpi-survey-full
TSRC    = $(TARGET).tex
#BIBS   = ref.bib 
LATEX  = pdflatex

CSV    = ../csv/MPI\ International\ Survey.csv
PROGDIR = ../..
PROG   = $(PROGDIR)/analyze.py
PSRC    = $(PROG).in
OPTS_ALL = -t -s all -c all
OPTS_TEX = -x -O ../inputs 
OPTS_PDF =  -o ../figs -f pdf
OPTS   =  $(OPTS_ALL)  $(OPTS_PDF) $(OPTS_TEX) $(INPUT)

PDF    = $(TARGET).pdf

all : $(PDF)

$(PROG) : $(PSRC)
	cd $(PROGDIR) ; ./build.sh

tex : $(PROG)
	$(PROG) $(OPTS_TEX) $(CSV)

pdf : $(PROG)
	$(PROG) $(OPTS_ALL) $(OPTS_PDF) $(CSV)

OUTPUT = ../inputs/Q1-ans.tex

$(OUTPUT) : $(PROG) $(CSV)
	$(PROG) $(OPTS) $(CSV)

$(PDF) : $(TSRC) $(BIBS) $(PROG) $(OUTPUT) Makefile
	$(LATEX) $(TARGET);		\
	bibtex $(TARGET);		\
	$(LATEX) $(TARGET);		\
	$(LATEX) $(TARGET);		\
	grep -e $(LATEX) -e "LaTeX\ Warning" -e "Package\ natbib\ Warning" -e "undefined" -e "multiply\ defined" $(TARGET).log;	\

clean:
	rm -f $(PDF) *.bbl *.blg *.out *.aux *.log *~ *.dvi

veryclean: clean
	rm -f $(PDF) ../inputs/Q*.tex ../figs/Q*.pdf

PDF    = $(TARGET).pdf
