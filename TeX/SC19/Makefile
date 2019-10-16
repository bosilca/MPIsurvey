TARGET = sc19-interim
SRCS    = $(TARGET).tex
BIBS   = ../ref.bib
LATEX  = pdflatex
DVI    = $(TARGET).dvi
PDF    = $(TARGET).pdf

all : $(PDF)

$(PDF) : $(SRCS) $(BIBS) Makefile
	$(LATEX) $(TARGET);
	bibtex $(TARGET);
	$(LATEX) $(TARGET);
	$(LATEX) $(TARGET);
	grep -e $(LATEX) -e "LaTeX\ Warning" -e "Package\ natbib\ Warning" \
	     -e "undefined" -e "multiply\ defined" $(TARGET).log;

clean :
	rm -f $(PDF) *.bbl *.blg *.out *.aux *.log *~ *.dvi
