# Developer Environment Setup Guide for niceML 🍦

## Overview

👋 Welcome to the development environment setup guide for niceML! This guide will walk you through the process of setting up a development environment for contributing to our open-source project. We use Poetry for managing dependencies, and we recommend using conda environments for a seamless development experience. Let's get your environment up and running smoothly! 🚀

## Prerequisites

Before you begin, ensure that you have the following installed on your system:

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (miniconda or anaconda)

## Clone the Repository

```bash
git clone https://github.com/codecentric-oss/niceml.git
cd niceml
```

## Create a Conda Environment

We recommend using conda to manage your Python environment. Navigate to the project directory and create a conda environment:

```bash
conda create --name your-env-name python=3.x
conda activate your-env-name
```

Replace `your-env-name` with your desired environment name and `3.x` with a Python version above 3.8 and below 3.11.

## Install Poetry Dependencies

We recommend to don't use Poetry environments. Deactive the creation of poetry environments:

```bash
poetry config virtualenvs.create false
```

Once your conda environment is active, use Poetry to install project dependencies:

### Default dependency installation
```bash
poetry install -E tensorflow -E visu
```

### Dependency installation for Apple Silicon 
```bash
poetry install -E tensorflow-macos -E visu
```

This will install all the required dependencies specified in the `pyproject.toml` file.

## Running Tests

Ensure everything is set up correctly by running the tests:

```bash
pytest
```

If all tests pass, you're ready to start contributing to the project! 🎉

## Contributing Guidelines

Before you start contributing, make sure to check our [contribution guidelines](CONTRIBUTION.md) for information on coding standards, pull request procedures, and more.

Happy coding! 🚀👩‍💻👨‍💻
