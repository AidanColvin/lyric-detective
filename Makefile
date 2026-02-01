PYTHON := ./venv/bin/python
PIP := ./venv/bin/python -m pip
PYTEST := ./venv/bin/pytest
PYTEST_FLAGS := -vv -x -s
REPL := ./venv/bin/ptpython

.PHONY: setup run repl clean

$(PYTHON):
	python3 -m venv venv

$(PYTEST) $(REPL): | $(PYTHON)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

setup: $(PYTEST) $(REPL)

run: | $(PYTHON)
	$(PYTHON) authorship.py texts

un: | $(PYTHON)
	$(PYTHON) authorship.py texts --test-all

sig: | $(PYTHON)
	$(PYTHON) authorship.py texts --print-signatures

repl: | $(REPL)
	$(REPL)

clean:
	rm -rf venv
