TARGET = swopp-ahori
SRCS    = $(TARGET).tex
BIBS   = ../ref.bib
LATEX  = platex
DVI2PDF = dvipdfmx
#LATEX  = pdflatex
XBB    = extractbb
DVI    = $(TARGET).dvi
PDF    = $(TARGET).pdf

all : $(PDF)

$(PDF) : $(DVI)
	$(DVI2PDF) $(DVI)

bbox :
	cd ../pdfs/; $(XBB) *.pdf

$(DVI) : $(SRCS) $(BIBS) Makefile
	$(LATEX) $(TARGET);		\
	bibtex $(TARGET);		\
	$(LATEX) $(TARGET);		\
	$(LATEX) $(TARGET);		\
	grep -e $(LATEX) -e "LaTeX\ Warning" -e "Package\ natbib\ Warning" -e "undefined" -e "multiply\ defined" $(TARGET).log;	\

clean :
	rm -f $(PDF) *.bbl *.blg *.out *.aux *.log *~ *.dvi ../pdfs/*.bb ../pdfs/*.xbb
