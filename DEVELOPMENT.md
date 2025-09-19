# Development Guide for OpenWebUI Python SDK

This guide provides instructions for setting up and working with the OpenWebUI Python SDK in a development environment.

## Setting Up a Development Environment

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- virtualenv or venv (recommended)

### Setting Up a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Installing Development Dependencies

```bash
# Install development dependencies
pip install -r requirements.txt

# Install test dependencies
pip install pytest pytest-cov pytest-mock
```

## Building and Installing the Package

### Option 1: Install in Development Mode

This is the recommended approach during development as it allows you to make changes to the code without reinstalling the package.

```bash
# Install the package in development mode
pip install -e .
```

### Option 2: Build and Install the Package

If you want to build and install the package as if it were coming from PyPI:

```bash
# Build the package
python setup.py sdist bdist_wheel

# Install the built package
pip install dist/openwebui_python-*.whl
```

## Running the Test Script

After installing the package in development mode, you can run the test script:

1. First, create your `.env` file:

```bash
# Copy the example .env file
cp .env.example .env
# Edit the .env file with your API credentials
```

2. Then run the test script:

```bash
python main.py
```

## Running Tests

To run the unit tests:

```bash
# Run all tests
pytest tests/

# Run tests with coverage report
pytest --cov=openwebui_python tests/

# Run a specific test file
pytest tests/test_client.py
```

## Manual Testing in Python REPL

You can also test the SDK interactively in the Python REPL:

```bash
# Start Python REPL
python

# In the REPL
>>> from openwebui_python import OpenWebUI
>>> client = OpenWebUI(base_url="your-url", api_key="your-key")
>>> models = client.get_models()
>>> print(models[0].name)
```

## Building Distribution for Release

When you're ready to build a distribution for release:

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build source and wheel distributions
python setup.py sdist bdist_wheel

# The distributable packages will be in the dist/ directory
```

## Using module_build_script.sh

The repository includes a `module_build_script.sh` script that automates the build process:

```bash
# Make the script executable (if needed)
chmod +x module_build_script.sh

# Run the build script
./module_build_script.sh
