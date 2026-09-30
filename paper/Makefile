PAPER  = main
OUT    = ../docs/release-gates-physical-ai.pdf
BUILD  = build

.PHONY: all clean watch

all: $(OUT)

$(OUT): $(PAPER).tex refs.bib
	@mkdir -p $(BUILD) ../docs
	tectonic -X compile $(PAPER).tex --outdir $(BUILD) --keep-logs
	@cp $(BUILD)/$(PAPER).pdf $(OUT)
	@echo "built -> $(OUT)"

watch:
	tectonic -X watch

clean:
	rm -rf $(BUILD)
