# Commit Guidelines for niceML 🍦

## Overview

👋 Welcome to the commit guidelines for niceML! We follow the Conventional Commits specification, a lightweight convention on top of commit messages. The commit messages play a crucial role in determining the project version for a new release and are used to generate the CHANGELOG. Let's dive into the details of how to structure your commits.

## Commit Message Structure

A commit message consists of a **header**, an optional **body**, and an optional **footer**. The header has a special format that includes a **type**, an **optional scope**, and a **short description**:

```
<type>(<scope>): <description>
```

### Type

The **type** must be one of the following:

- **build**: Changes related to the build system or external dependencies.
- **chore**: Routine tasks, maintenance, or refactors.
- **ci**: Changes to the project's CI/CD configuration.
- **docs**: Documentation changes.
- **feat**: A new feature for the user.
- **fix**: A bug fix.
- **perf**: Performance-related improvements.
- **style**: Code style changes (formatting).
- **refactor**: Code refactoring without changing external behavior.
- **test**: Adding or modifying tests.

### Scope (Optional)

The **scope** provides additional context about the location of the change. It can be omitted if the change is general or affects multiple components.

### Description

The **description** is a concise, present-tense summary of the change. It should be clear and easy to understand.

## Examples

Here are some examples of well-formed commit messages:

- **feat(user-auth): add social media login options**
- **fix(api): resolve issue with incorrect response format**
- **chore: update dependencies to latest versions**
- **docs(readme): improve project setup instructions**
- **style: format code using black**
- **test(unit): add test coverage for module X**
- **ci: configure GitHub Actions for continuous integration**

## Committing Changes

When making changes, please follow these guidelines:

1. **Separate Changes**: If a commit includes multiple changes, try to group them logically and make separate commits.

2. **Be Clear and Concise**: Write clear and concise commit messages. Avoid unnecessary details in the header.

3. **Use Imperative Mood**: Write the description in the imperative mood, e.g., "fix bug" instead of "fixed bug."

4. **Avoid WIP commits**: To have a clean GIT history, please avoid _WIP_ commits or other commits that are not conventional commits. 
   If the Git history contains commits that are not conventional commits, your code contribution will be squashed when the pull request is merged.

## Versioning and Changelog

The version number for a new release is determined based on the types of commits since the last release. Follow semantic versioning (major.minor.patch). The CHANGELOG is automatically generated from commit messages.

## Examples

Here are some examples of versioning based on commit messages:

- **feat**: Increment the minor version (1.2.0).
- **fix**: Increment the patch version (1.1.1).
- **chore**: No version change.

For more details, refer to the [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/).

Thank you for following these commit guidelines! 🚀✨
