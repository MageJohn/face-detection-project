PDC := pandoc
PDC_FLAGS := --pdf-engine=xelatex

.PHONY: default clean

default: report.pdf

report.pdf: report.md
	${PDC} ${PDC_FLAGS} $< -o $@

report.tex: report.md
	${PDC} ${PDC_FLAGS} $< -s -o $@

clean:
	rm -f report.pdf
