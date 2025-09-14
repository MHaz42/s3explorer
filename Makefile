SHELL=/bin/bash

.PHONY: build
build:
	@echo -e "\n========== Building project ==========\n"
	python3 -m build


.PHONY: install
install: build
	$(eval WHEEL = $(shell ls -rt dist/* | tail -n1))
	@echo -e "\n========== Installing $(WHEEL) ==========\n"
	pip3 install --force-reinstall $(WHEEL)


.PHONY: run
run:
	textual run --dev src/s3explorer/__main__.py