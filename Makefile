PYTHON ?= python3
TECTONIC ?= tectonic
PDFTOPPM ?= pdftoppm
SOURCE ?= templates/master-resume.md
PROFILE ?= templates/profile.json
NAME ?= resume
EXPECTED ?=

.PHONY: demo qa resume setup test robotics sales-engineering crypto crypto-venture-fund

setup:
	$(PYTHON) -m pip install -r requirements.txt

demo: robotics

qa: robotics sales-engineering crypto crypto-venture-fund

robotics sales-engineering crypto:
	$(MAKE) resume SOURCE=examples/sample-candidate/master-resume.md PROFILE=examples/sample-candidate/profiles/$@.json NAME=$@ EXPECTED=examples/sample-candidate/expected/$@.json

crypto-venture-fund:
	$(MAKE) resume SOURCE=examples/sample-candidate/crypto-venture-fund.md PROFILE=examples/sample-candidate/profiles/crypto-venture-fund.json NAME=crypto-venture-fund EXPECTED=examples/sample-candidate/expected/crypto-venture-fund.json

resume:
	$(PYTHON) scripts/build_resume.py --source "$(SOURCE)" --profile "$(PROFILE)" --tex "build/$(NAME).tex"
	mkdir -p output/pdf "tmp/pdfs/$(NAME)"
	$(TECTONIC) --outdir output/pdf "build/$(NAME).tex"
	$(PYTHON) scripts/validate_resume.py "output/pdf/$(NAME).pdf" --text-output "tmp/pdfs/$(NAME)/resume.txt" $(if $(EXPECTED),--expected "$(EXPECTED)",)
	$(PDFTOPPM) -png -r 150 "output/pdf/$(NAME).pdf" "tmp/pdfs/$(NAME)/page"

test:
	$(PYTHON) -m unittest discover -s tests -v
