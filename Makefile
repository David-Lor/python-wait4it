.DEFAULT_GOAL := help

install-test-requirements:
	pip install -r tests/requirements.txt

test:
	pytest -sv .

help: ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'