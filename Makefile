PDC := pandoc
PDC_FLAGS := --pdf-engine=xelatex -F pantable -F pandoc-plot -F pandoc-crossref --citeproc

.PHONY: default clean

default: report.pdf reflections.pdf

COMMON_PREREQS := report.md macros.md metadata.yaml bibliography.yaml ieee.csl

report.pdf: ${COMMON_PREREQS}
	${PDC} ${PDC_FLAGS} metadata.yaml macros.md $< -o $@

report.tex: ${COMMON_PREREQS}
	${PDC} ${PDC_FLAGS} metadata.yaml macros.md $< -s -o $@

reflections.pdf: reflections.md
	${PDC} --pdf-engine=xelatex $< -s -o $@

SRC_DIR := $(shell find src/experiments -maxdepth 1 -name '*.py') \
					 src/README.md src/pyproject.toml src/setup.py

submission.zip: report.pdf reflections.pdf ${SRC_DIR} Datasets/download_datasets.sh
	zip $@ $?

ieee.csl:
	wget https://www.zotero.org/styles/ieee -O $@

clean:
	rm -f report.pdf
	rm -rf images/plot/
