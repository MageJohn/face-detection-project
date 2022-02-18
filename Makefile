PDC := pandoc
PDC_FLAGS := 

.PHONY: default clean

default: report.pdf

report.pdf: report.md
	${PDC} ${PDC_FLAGS} $< -o $@

clean:
	rm -f report.pdf
