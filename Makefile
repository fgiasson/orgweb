.PHONY: install-build build install-local-build uninstall-local-build rebuild-local create-ven source-venv clean
install-build:
	pip install --upgrade build

build: 
	python3 -m build

install-local-build:
	pip install .

uninstall-local-build:
	pip uninstall -y weborg

rebuild-local:
	pip uninstall -y weborg
	python3 -m build
	pip install .
	
create-venv:
	python3 -m venv .venv

source-venv:
	source .venv/bin/activate

clean:
	rm -rf build 
	rm -rf dist 
	rm -rf weborg.egg-info
	rm -rf weborg/__pycache__