#!/bin/bash

# Script to run regression tests
# These tests verify that critical functionality continues to work after code changes

set -e # Exit on any error

echo "=== Running Regression Tests ==="

echo "Creating Python virtual environment..."
python -m venv .venv

echo "Activating virtual environment..."
. .venv/bin/activate

echo "Installing test dependencies..."
pip install -r tests/requirements-dev.txt

echo "Running regression tests..."
cd tests && python -m pytest regression.py -v --tb=short --html=../regression-test-report.html --self-contained-html

echo "Regression tests completed successfully!"
echo "📊 Test report generated: regression-test-report.html"
