#!/usr/bin/env bash

echo "Installing dependencies for '${TRAVIS_PYTHON_VERSION}'"
if [[ ${TRAVIS_PYTHON_VERSION} == 2* ]]; then
    pip install -r requirements-python2.txt
fi
if [[ ${TRAVIS_PYTHON_VERSION} == 3* ]]; then
    pip install -r requirements-python3.txt
fi

echo "Installing test requirements"
pip install -r .travis/requirements-test.txt
