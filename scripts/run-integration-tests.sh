#!/bin/bash

# Script to run integration tests with Neon database
# This script is designed to be run in CI with a Neon database URL

set -e # Exit on any error

echo "=== Running Neon Integration Tests ==="

# Check if DATABASE_URL is set and is a PostgreSQL URL
if [ -z "$DATABASE_URL" ]; then
	echo "ERROR: DATABASE_URL environment variable is not set"
	echo "Integration tests require a Neon/PostgreSQL database URL"
	exit 1
fi

if [[ ! "$DATABASE_URL" =~ postgresql:// ]] && [[ ! "$DATABASE_URL" =~ postgres:// ]]; then
	echo "ERROR: DATABASE_URL does not appear to be a PostgreSQL URL"
	echo "Current DATABASE_URL: $DATABASE_URL"
	echo "Integration tests require a Neon/PostgreSQL database URL"
	exit 1
fi

echo "Using database URL: ${DATABASE_URL}"

echo "Creating Python virtual environment..."
python -m venv .venv

echo "Activating virtual environment..."
. .venv/bin/activate

echo "Installing test dependencies..."
pip install -r tests/requirements-dev.txt

ATLAS_URL="${DATABASE_URL}&search_path=public" # Atlas requires schema to be specified in the URL for NeonDB

echo "Checking if migrations are up to date with SQLAlchemy models..."
atlas migrate diff --env postgres

echo "Applying database migrations to Neon..."
atlas migrate apply --env postgres --url "$ATLAS_URL"

echo "Running integration tests..."
cd tests && python -m pytest integration.py -v --tb=short --html=../integration-test-report.html --self-contained-html

echo "Integration tests completed successfully!"
