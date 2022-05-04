PDC := pandoc
PDC_FLAGS := --pdf-engine=xelatex -F pandoc-plot -F pandoc-crossref --citeproc

.PHONY: default clean

default: report.pdf

COMMON_PREREQS := report.md bibliography.yaml ieee.csl gnuplot/render_pts.gp

report.pdf: ${COMMON_PREREQS}
	${PDC} ${PDC_FLAGS} $< -o $@

report.tex: ${COMMON_PREREQS}
	${PDC} ${PDC_FLAGS} $< -s -o $@

ieee.csl:
	wget https://www.zotero.org/styles/ieee -O $@

clean:
	rm -f report.pdf
	rm -rf plot/
