# Copilot Guidelines for Portfolio Ultime

## Build/Lint/Test Commands

Always source .venv and use devbox run before running commands.

```bash
source .venv/bin/activate
devbox run <command>
```

### Linting

```bash
ruff check .                    # Lint all files
ruff check app/                 # Lint app directory only
ruff format --check .           # Check formatting
ruff format .                   # Auto-format code
```

### Testing

```bash
# All test suites
./scripts/run-units-tests.sh     # Unit tests with coverage
./scripts/run-integration-tests.sh  # Integration tests (requires DATABASE_URL)
./scripts/run-regression-tests.sh    # Regression tests
./scripts/run-smoke-test.sh      # Docker smoke test (requires IMAGE and NAME)

# Single test execution
cd tests && python -m pytest units.py::test_home_route -v
cd tests && python -m pytest integration.py::test_database_connection -v
cd tests && python -m pytest regression.py::test_critical_endpoints -v

# Test with coverage
cd tests && python -m pytest units.py --cov=../app --cov-report=term
```

### Development

```bash
# Run application locally
cd app && python app.py

# Install dependencies
pip install -r app/requirements.txt
pip install -r tests/requirements-dev.txt
```

## Code Style Guidelines

### Python Version & Imports

- Python 3.13+ required
- Import order: standard library → third-party → local modules
- Use absolute imports within the app package
- Group imports with blank lines between groups

### Formatting & Line Length

- Max line length: 88 characters (Black/Ruff compatible)
- Use double quotes for strings unless single quotes are needed
- Trailing commas in multi-line structures

### Type Hints

- Use type hints for function parameters and return values
- Use `-> ReturnType` syntax for return type annotations
- Import types from `typing` module when needed

### Naming Conventions

- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### Error Handling

- Use try/except blocks for database operations
- Log errors with appropriate log levels
- Rollback database transactions on errors
- Return appropriate HTTP status codes

### Database Models

- Use SQLAlchemy with proper `__tablename__`
- Include `__repr__` methods for debugging
- Use nullable=False for required fields
- Add docstrings to model classes

### Flask Routes

- Use explicit HTTP method lists
- Add docstrings to route functions
- Handle form data validation
- Use `url_for()` for URL generation
- Return appropriate response types (JSON for API, templates for HTML)

### Testing

- Use descriptive test function names: `test_<action>_<context>`
- Include logging in test functions for debugging
- Use pytest fixtures from conftest.py
- Test both success and error cases
- Mock external dependencies when needed

### Documentation

- Use docstrings for all public functions and classes
- Follow Google/NumPy docstring format
- Document parameters, return values, and exceptions
- Keep README.md updated with project changes

## Key Reminders

- Always run linting and type checking after code changes
- Follow the established naming conventions and import order
- Include proper error handling in database operations
- Write comprehensive tests for new features
- Update documentation as the project evolves
