TARGET = MPI-Survey
SRCS    = $(TARGET).tex
BIBS   = ref.bib
LATEX  = pdflatex
DVI    = $(TARGET).dvi
PDF    = $(TARGET).pdf
BBL    = $(TARGET).bbl

GRAPHDIR = ../pdfs

all : $(PDF)

$(PDF) : $(SRCS) $(BIBS) Makefile
	$(LATEX) $(TARGET);
	bibtex $(TARGET)
	$(LATEX) $(TARGET);
	$(LATEX) $(TARGET);
	@grep -e $(LATEX) -e "LaTeX\ Warning" -e "Package\ natbib\ Warning" \
	     -e "undefined" -e "multiply\ defined" $(TARGET).log;

GRAPHS = $(GRAPHDIR)/TimeSeries.pdf \
	 $(GRAPHDIR)/Q1.pdf \
	 $(GRAPHDIR)/Q3.pdf \
	 $(GRAPHDIR)/Q3-Q16.pdf \
	 $(GRAPHDIR)/Q6.pdf \
	 $(GRAPHDIR)/Q6-Q3.pdf \
	 $(GRAPHDIR)/Q7.pdf \
	 $(GRAPHDIR)/Q9.pdf \
	 $(GRAPHDIR)/Q10.pdf \
	 $(GRAPHDIR)/Q12.pdf \
	 $(GRAPHDIR)/Q13.pdf \
	 $(GRAPHDIR)/Q14.pdf \
	 $(GRAPHDIR)/Q15.pdf \
	 $(GRAPHDIR)/Q17.pdf \
	 $(GRAPHDIR)/Q18.pdf \
	 $(GRAPHDIR)/Q19.pdf \
	 $(GRAPHDIR)/Q21.pdf \
	 $(GRAPHDIR)/Q22.pdf \
	 $(GRAPHDIR)/Q22-Q24.pdf \
	 $(GRAPHDIR)/Q23.pdf \
	 $(GRAPHDIR)/Q24.pdf \
	 $(GRAPHDIR)/Q25.pdf \
	 $(GRAPHDIR)/Q26.pdf \
	 $(GRAPHDIR)/Q27.pdf \
	 $(GRAPHDIR)/Q28.pdf \
	 $(GRAPHDIR)/Q29.pdf

figs :
	rm Figs/Q*.pdf
	cp $(GRAPHS) Figs/
.PHONY: figs

clean :
	rm -f $(PDF) *.bbl *.blg *.out *.aux *.log *.spl *~ *.dvi
