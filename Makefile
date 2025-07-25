PYTHON = python3
PIP = pip
SRC_DIR = src

run:
	$(PYTHON) $(SRC_DIR)/main.py

install:
	$(PIP) install -r requirements.txt

.PHONY: all run install