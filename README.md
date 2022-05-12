# CollateX Utils

[![PyPI version](https://badge.fury.io/py/acdh-collatex-utils.svg)](https://badge.fury.io/py/acdh-collatex-utils)
[![codecov](https://codecov.io/gh/acdh-oeaw/acdh_collatex_utils/branch/master/graph/badge.svg?token=G3PO6ZC12Z)](https://codecov.io/gh/acdh-oeaw/acdh_collatex_utils)

A python package to collate things with collate-x

## install

* create a virtual environment and install the package with `pip install acdh_collatex_utils` 

## use

To collate a bunch of XML/TEI documents located in e.g. `./to_collate` run
`collate -g './to_collate/*.xml`

This creates a folder `./to_collate/collated` and saves chunked HTML and TEI Files like `out__001.html` or `out__001.tei`

To see this package in use in a real life project, please check out [frd-data/collate_work.py](https://github.com/freud-digital/frd-data/blob/main/collate_work.py)

## develop

* create a virutal environment
* install dev-requirements `pip install -U pip` and `pip install -r requirements_dev.txt`
* install the package in dev-mode `pip install -e .`

* run test with `coverage run -m pytest -v`
* create test-report `coverage report` or `coverage html`