.DEFAULT_GOAL := help

install-test-requirements: ## pip install requirements for tests
	pip install -r tests/requirements.txt

test: ## run tests
	pytest -sv .

install-package-requirements: ## pip install requirements for packaging & uploading
	pip install --upgrade pip setuptools wheel twine

package: ## create package (sdist)
	python setup.py sdist bdist_wheel

package-upload: ## upload package to pypi
	twine upload --skip-existing dist/*

package-test-upload: ## upload package to test-pypi
	twine upload --skip-existing --repository testpypi dist/*

package-clear: ## clear dist directory
	rm -rf dist/ build/ *.egg-info/ MANIFEST

help: ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
