# Running OpenWebUI Python SDK Tests

This directory contains tests for the OpenWebUI Python SDK. The tests are written using pytest and follow best practices for testing Python packages.

## Prerequisites

Before running the tests, make sure you have the required packages installed:

```bash
pip install pytest pytest-cov pytest-mock
```

## Running All Tests

To run all tests, navigate to the root directory of the project and run:

```bash
pytest tests/
```

## Running Specific Test Files

To run tests from a specific file:

```bash
pytest tests/test_client.py
```

## Running Specific Test Classes or Methods

To run a specific test class:

```bash
pytest tests/test_client.py::TestBaseClient
```

To run a specific test method:

```bash
pytest tests/test_client.py::TestBaseClient::test_init_with_params
```

## Coverage Report

To generate a test coverage report:

```bash
pytest --cov=openwebui_python tests/
```

For a more detailed HTML coverage report:

```bash
pytest --cov=openwebui_python --cov-report=html tests/
```

This will create an `htmlcov` directory with an HTML report that you can open in your browser.

## Test Organization

The tests are organized by module, following the same structure as the package:

- `tests/test_client.py`: Tests for the base client functionality
- `tests/test_api_*.py`: Tests for API domain modules
- `tests/test_utils_*.py`: Tests for utility modules
- `tests/conftest.py`: Shared fixtures for all tests

## Creating New Tests

When adding new features to the SDK, please also add corresponding tests. Follow the existing patterns for consistency:

1. Use descriptive test method names (e.g., `test_get_models_success`)
2. Group related tests in test classes
3. Add docstrings to test methods to describe what they're testing
4. Use fixtures from `conftest.py` where applicable
5. Mock external dependencies appropriately
