.PHONY: all targets tests
.SUFFIXES:
.SECONDARY:

all: targets tests

targets: \
 kson/grammar/json.py \
 kson/grammar/kson.py

kson/grammar/%.py: grammar/%.lark
	python -m lark.tools.standalone $< > $@
