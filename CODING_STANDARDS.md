# Coding Guidelines for niceML 🍦

Welcome to the coding guidelines for niceML! To ensure consistency and
maintainability across the codebase, please follow these guidelines when contributing to
the project. 🚧💻

## Table of Contents

- [Style Guide](#style-guide)
- [Naming Conventions](#naming-conventions)
- [Documentation](#documentation)
- [Testing](#testing)
- [Code Organization](#code-organization)
- [Dependencies](#dependencies)
- [Security](#security)

## Style Guide

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python
code. Please run a linter before submitting your code changes.

## Naming Conventions

- Use descriptive and meaningful variable and function names.
- Follow the snake_case convention for variable and function names.
- Class names should follow the CamelCase convention.

```python
# Good
def calculate_average(numbers_list):
    pass


class DataProcessor:
    pass


# Avoid
def calc_avg(nums):
    pass


class data_processor:
    pass
```

## Pre-Commit Hooks

We use of pre-commit hooks to maintain code quality and
consistency throughout the project. Pre-commit hooks automate checks and formatting
tasks before each commit, preventing issues from being introduced into the repository.
This ensures that all contributors follow the established coding standards and 
contribute to a cleaner and more consistent codebase. Make sure to run
pre-commit checks before each commit to avoid common issues and keep the development
process smooth. 🧹👩‍💻👨‍💻

To set up pre-commit hooks:

**Install Pre-Commit:**
```bash
poetry run pre-commit install
```

**Run Pre-Commit on Existing Code: (Optional)**
```bash
poetry run pre-commit run --all-files
```
   
**Run Pre-Commit on your staged Code Changes: (Required for each Commit)**
```bash
poetry run pre-commit run
```

## Documentation

- Include docstrings for all modules, classes, and functions using
  the [Google Style Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
- Provide clear and concise comments for complex or non-obvious code sections.

## Testing

- Write unit tests for new features and bug fixes.
- Ensure existing tests pass before submitting a pull request.
- Strive for high test coverage to catch potential issues early.
- Make sure all tests ran successfully, before a Merge.

## Code Organization

- Keep each module focused on a specific functionality.
- Group related functions and classes together.
- Generalize where it is reasonable and possible.
- Avoid overly long functions; consider breaking them into smaller, more modular
  functions.

## Dependencies

- Use [Poetry](https://python-poetry.org/) for managing project dependencies.
- Document dependencies in the `pyproject.toml` file.
- [Pin versions](https://python-poetry.org/docs/cli/#add) to ensure consistent behavior across environments.

```bash
poetry add <new-package>
```

## Security

- Be mindful of potential security vulnerabilities in your code.
- If you discover a security issue, please report it responsibly by contacting the
  maintainers privately via our Email [contact-niceml@codecentric.de](mailto:contact-niceml@codecentric.de).

These guidelines are designed to ensure a clean and maintainable codebase. Thank you for
your commitment to writing high-quality code for niceML! 🌈👩‍💻👨‍💻
