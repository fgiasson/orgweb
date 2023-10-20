# [[file:org/Makefile.org::*Phony][Phony:1]]
.PHONY: install-build build install-local-build uninstall-local-build rebuild-local create-ven source-venv clean
# Phony:1 ends here

# [[file:org/Makefile.org::*install-build][install-build:1]]
install-build:
	pip install --upgrade build
# install-build:1 ends here

# [[file:org/Makefile.org::*create-env][create-env:1]]
create-venv:
	python3 -m venv .venv
# create-env:1 ends here

# [[file:org/Makefile.org::*source-env][source-env:1]]
source-venv:
	source .venv/bin/activate
# source-env:1 ends here

# [[file:org/Makefile.org::*build][build:1]]
build:
	python3 -m build
# build:1 ends here

# [[file:org/Makefile.org::*install-local-build][install-local-build:1]]
install-local-build:
	pip install .
# install-local-build:1 ends here

# [[file:org/Makefile.org::*uninstall-local-build][uninstall-local-build:1]]
uninstall-local-build:
	pip uninstall -y weborg
# uninstall-local-build:1 ends here

# [[file:org/Makefile.org::*rebuild-local][rebuild-local:1]]
rebuild-local:
	pip uninstall -y weborg
	python3 -m build
	pip install .
# rebuild-local:1 ends here

# [[file:org/Makefile.org::*Clean][Clean:1]]
clean:
	rm -rf build
	rm -rf dist
	rm -rf weborg.egg-info
	rm -rf org/weborg/__pycache__
	rm -rf weborg
	rm -rf resources
	rm -rf .mypy_cache
	rm Dockerfile
	rm pyproject.toml
# Clean:1 ends here
