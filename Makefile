PDC := pandoc
PDC_FLAGS := --pdf-engine=xelatex -F pandoc-plot -F pandoc-crossref --citeproc

.PHONY: default clean

default: report.pdf

COMMON_PREREQS := report.md macros.md metadata.yaml bibliography.yaml ieee.csl images/gnuplot/*

report.pdf: ${COMMON_PREREQS}
	${PDC} ${PDC_FLAGS} metadata.yaml macros.md $< -o $@

report.tex: ${COMMON_PREREQS}
	${PDC} ${PDC_FLAGS} metadata.yaml macros.md $< -s -o $@

ieee.csl:
	wget https://www.zotero.org/styles/ieee -O $@

clean:
	rm -f report.pdf
	rm -rf images/plot/
