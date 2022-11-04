all:
	@echo nothing special

clean:
	rm -rf build dist wheelhouse *.egg-info
force_clean:
	docker run --rm -v `pwd`:`pwd` -w `pwd` -it alpine/make make clean
.PHONY: clean force_clean

lint:
	pre-commit run -a
lint_install:
	pre-commit install

build:
	mkdir -p build && cd build && \
	cmake .. && make
.PHONY: build

DOCKER_TAG_WINDOWS ?= ghcr.io/cubao/build-env-windows-x64:v0.0.1
DOCKER_TAG_LINUX ?= ghcr.io/cubao/build-env-manylinux2014-x64:v0.0.1
DOCKER_TAG_MACOS ?= ghcr.io/cubao/build-env-macos-arm64:v0.0.1

test_in_win:
	docker run --rm -w `pwd` -v `pwd`:`pwd` -v `pwd`/build/win:`pwd`/build -it $(DOCKER_TAG_WINDOWS) bash
test_in_mac:
	docker run --rm -w `pwd` -v `pwd`:`pwd` -v `pwd`/build/mac:`pwd`/build -it $(DOCKER_TAG_MACOS) bash
test_in_linux:
	docker run --rm -w `pwd` -v `pwd`:`pwd` -v `pwd`/build/linux:`pwd`/build -it $(DOCKER_TAG_LINUX) bash

PYTHON ?= python3
python_install:
	$(PYTHON) setup.py install
python_build:
	$(PYTHON) setup.py bdist_wheel
python_sdist:
	$(PYTHON) setup.py sdist
	# tar -tvf dist/pybind11_rdp-*.tar.gz
python_test:
	$(PYTHON) -c 'from pybind11_rdp import rdp; print(rdp([[1, 1], [2, 2], [3, 3], [4, 4]]))'
	$(PYTHON) test.py

# conda create -y -n py36 python=3.6
# conda create -y -n py37 python=3.7
# conda create -y -n py38 python=3.8
# conda create -y -n py39 python=3.9
# conda create -y -n py310 python=3.10
# conda env list
python_build_py36:
	PYTHON=python conda run --no-capture-output -n py36 make python_build
python_build_py37:
	PYTHON=python conda run --no-capture-output -n py37 make python_build
python_build_py38:
	PYTHON=python conda run --no-capture-output -n py38 make python_build
python_build_py39:
	PYTHON=python conda run --no-capture-output -n py39 make python_build
python_build_py310:
	PYTHON=python conda run --no-capture-output -n py310 make python_build
python_build_all: python_build_py36 python_build_py37 python_build_py38 python_build_py39 python_build_py310
python_build_all_in_linux:
	docker run --rm -w `pwd` -v `pwd`:`pwd` -v `pwd`/build/win:`pwd`/build -it $(DOCKER_TAG_LINUX) make python_build_all
	make repair_wheels && rm -rf dist/*.whl && mv wheelhouse/*.whl dist && rm -rf wheelhouse
python_build_all_in_macos: python_build_py38 python_build_py39 python_build_py310
python_build_all_in_windows: python_build_all

repair_wheels:
	python -m pip install auditwheel # sudo apt install patchelf
	ls dist/* | xargs -n1 auditwheel repair --plat manylinux2014_x86_64

pypi_remote ?= pypi
upload_wheels:
	python -m pip install twine
	twine upload dist/*.whl -r $(pypi_remote)

tar.gz:
	tar -cvz --exclude .git -f ../pybind11-rdp.tar.gz .
	ls -alh ../pybind11-rdp.tar.gz

# https://stackoverflow.com/a/25817631
echo-%  : ; @echo -n $($*)
Echo-%  : ; @echo $($*)
ECHO-%  : ; @echo $* = $($*)
echo-Tab: ; @echo -n '    '
