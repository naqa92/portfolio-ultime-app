#!/bin/bash

# Script to run unit tests with coverage and HTML reports
# This script sets up the Python environment and runs pytest with coverage

set -e # Exit on any error

echo "=== Running Units Tests ==="

echo "Creating Python virtual environment..."
python -m venv .venv

echo "Activating virtual environment..."
. .venv/bin/activate # . is a shorthand for 'source'

echo "Installing test dependencies..."
pip install -r tests/requirements-dev.txt

echo "Running unit tests with pytest, coverage and HTML reports..."
cd tests && python -m pytest units.py -v --tb=short --cov=../app --cov-config=../.coveragerc --cov-report=html:../coverage-html --cov-report=term --html=../units-test-report.html --self-contained-html
