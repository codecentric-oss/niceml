# CHANGELOG


## v0.17.0-dev.6 (2024-12-03)

### Bug Fixes

- `read_image` and `write_image` now use `LocalFileSystem` as default
  ([#140](https://github.com/codecentric-oss/niceml/pull/140),
  [`a0978b9`](https://github.com/codecentric-oss/niceml/commit/a0978b9bc16f8b97d7dec5bc60e5e03f9128f9a8))

## 📥 Pull Request Description

Currently you cannot use `read_image` and `write_image` without specifying a FileSystem. The default
  (`LocalFileSystem`) was not used correctly. This is now fixed in this PR.

## 👀 Affected Areas

- ioutils

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [X] All tests ran successfully - [X] All merge conflicts are
  resolved - [X] Documentation has been updated to reflect the changes - [X] Any necessary
  migrations have been run


## v0.17.0-dev.5 (2024-09-12)

### Features

- Add the ability to add a niceML formatted timestamp based on a given datetime object
  ([`9cebe9d`](https://github.com/codecentric-oss/niceml/commit/9cebe9d8d688a21aec2f83ccd69cd23edab89cb5))

The timestmap format used in niceml has a special foramt. If it is necessary to create this, it can
  now be created based on a given datetime object.


## v0.17.0-dev.4 (2024-08-20)

### Bug Fixes

- Config tests
  ([`10b0d78`](https://github.com/codecentric-oss/niceml/commit/10b0d78f3486b01dd11aaf804bdbe61085362e35))

- Config tests for old config
  ([`af02edc`](https://github.com/codecentric-oss/niceml/commit/af02edc2c11d8e2fae9e7d986c0e4d81d870cdbe))

- Less static dependencies
  ([`e0becd7`](https://github.com/codecentric-oss/niceml/commit/e0becd7485b951e169a209f73bd7e4255c3a6c4d))


## v0.17.0-dev.3 (2024-08-15)

### Bug Fixes

- Make altair not optional
  ([`6b248d5`](https://github.com/codecentric-oss/niceml/commit/6b248d5ccc8fd6bc4d3b307b1c533fef28a6b9e8))


## v0.17.0-dev.2 (2024-08-12)

### Documentation

- Improve docstring for read and write functions
  ([`46f9f53`](https://github.com/codecentric-oss/niceml/commit/46f9f53c4ed3c25d4ea00043f85899ae89f79a26))

- Improve docstring for read and write functions
  ([`1840097`](https://github.com/codecentric-oss/niceml/commit/184009725ce0f1475455f9b1a5ff43a7bee5d5a6))

### Features

- Add write chart to exp context
  ([`f120835`](https://github.com/codecentric-oss/niceml/commit/f1208354be783d6bda51c7d947efe4fab8910469))

### Testing

- Test write_chart
  ([`d636f63`](https://github.com/codecentric-oss/niceml/commit/d636f634405e540b75d23fbca7714c9e4b39f94d))


## v0.17.0-dev.1 (2024-08-07)

### Features

- Add possibility to pass additional arguments when initializing a `ResultAnalyzer`
  ([#134](https://github.com/codecentric-oss/niceml/pull/134),
  [`6e48893`](https://github.com/codecentric-oss/niceml/commit/6e48893b6734a554eacaf30985926dd865f8a275))

## 📥 Pull Request Description

This PR adds the following features and changes:

- feat: Add possibility to pass additional arguments when initializing a `ResultAnalyzer` -
  refactor: Add an experiment context to the `initialize` function of the `DataframeAnalyzer` -
  refactor: Pass the experiment context of a train or eval pipeline run to the result analyzer.

## 👀 Affected Areas

- Result analyzers - Analyse op - Train and eval job


## v0.16.1-dev.1 (2024-07-23)

### Bug Fixes

- Change version ([#130](https://github.com/codecentric-oss/niceml/pull/130),
  [`7343560`](https://github.com/codecentric-oss/niceml/commit/7343560dcaf30bb29334348ed4387c6dc0f5361d))

## 📥 Pull Request Description

Please describe your changes in detail and provide any necessary context.

## 👀 Affected Areas

Please indicate which areas of the project are affected by your changes (e.g. dashboard, pipelines,
  tests, documentation).

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [ ] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

- Downgrade `python-semantic-release` and adjust build command
  ([#132](https://github.com/codecentric-oss/niceml/pull/132),
  [`b23fce4`](https://github.com/codecentric-oss/niceml/commit/b23fce47ad25de30964a532e79c25638b9f41cb9))

### Continuous Integration

- Adjust version_variables and version_toml for semantic-release
  ([#133](https://github.com/codecentric-oss/niceml/pull/133),
  [`3bf6d0e`](https://github.com/codecentric-oss/niceml/commit/3bf6d0e5a9cd30642f26a8f6226959df484283c4))

## 📥 Pull Request Description

- Replace version_variable by version_variables and version_toml

## 👀 Affected Areas

- pyproject.toml - CI/CD

- Fix prerelease flag in pre-release pipeline
  ([`f5fb645`](https://github.com/codecentric-oss/niceml/commit/f5fb6451d97b74045fd7b356bc6dea64f77ba14b))

- Update python-semantic-release and add pre-release pipeline for dev branch
  ([`16a28c1`](https://github.com/codecentric-oss/niceml/commit/16a28c14efbce9114d7a3a6741b067116e849166))

- Update used python version in docs pipeline
  ([`f6258a1`](https://github.com/codecentric-oss/niceml/commit/f6258a179b61ce0cd44944e001ed1387c840b3f2))

### Refactoring

- Allow `kwargs` in `write_image`
  ([`f1c13f0`](https://github.com/codecentric-oss/niceml/commit/f1c13f051e92dbed379b325f7032f420de997305))

- Update dependencies
  ([`485983b`](https://github.com/codecentric-oss/niceml/commit/485983b5a8dbfa8d12dc55765e7705fcb4682964))


## v0.16.0 (2024-06-13)

### Bug Fixes

- Localizeexperiment with location config
  ([`5edff9f`](https://github.com/codecentric-oss/niceml/commit/5edff9ff27c42b8558fbf3d640cbc689d58330b1))

### Features

- Add file loader
  ([`ea916b7`](https://github.com/codecentric-oss/niceml/commit/ea916b7edba9fbfa4b39c46e3c283aadd187c35a))


## v0.15.0 (2024-05-15)

### Features

- Allow freeze of model weights in training
  ([`1fee972`](https://github.com/codecentric-oss/niceml/commit/1fee972cafb87af971cf851088db41e12a3fdcb8))

## 📥 Pull Request Description

The following changes, features and fixes are part of this pull request:

- feat: allow freeze of model weights in training - docs: fix typo in documentation - ci: adjust
  workflow trigger - fix: change latest macos workflow image for test pipeline

## 👀 Affected Areas

- Documentation - Training - Github Workflow (Test pipeline)

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [x] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

---------

Co-authored-by: github-actions <action@github.com>

Co-authored-by: Nils Uhrberg <nils.uhrberg@codecentric.de>

Co-authored-by: Denis Stalz-John <denis.stalz-john@codecentric.de>


## v0.14.1 (2024-04-16)

### Bug Fixes

- Add original model id to eval experiment info
  ([`494c101`](https://github.com/codecentric-oss/niceml/commit/494c101fcd5993971cdb1b39895494cf6de82293))

- Load non-parq files with DFLoader load_df
  ([`b693710`](https://github.com/codecentric-oss/niceml/commit/b693710fdf03962a543579342ba95b359b634974))

- Test pipeline pendulum dependency
  ([`299426a`](https://github.com/codecentric-oss/niceml/commit/299426a27cfaf4f46e79958f600cdc1a8ad05466))

- Update poetry in Github pipelines to 1.7.1
  ([`2d0dd2e`](https://github.com/codecentric-oss/niceml/commit/2d0dd2e2f250fe7517c12b68f7d36802ddd73964))

### Code Style

- Typos and comment movement
  ([`300299d`](https://github.com/codecentric-oss/niceml/commit/300299db9ad791df75397d83358bffb4519e8654))


## v0.14.0 (2024-02-08)

### Bug Fixes

- Query experiments based on storage handler name not mutable id
  ([`1e94add`](https://github.com/codecentric-oss/niceml/commit/1e94addf39393e328a566b0190fdaf7aab4aa4ac))

- Simplify ExperimentManager using exp_dict
  ([`9a54dc9`](https://github.com/codecentric-oss/niceml/commit/9a54dc9ed954ab1a1a80a6964c9b7462d29b4b39))

### Features

- Update altair to 5.2.0 ([#113](https://github.com/codecentric-oss/niceml/pull/113),
  [`fbb72d4`](https://github.com/codecentric-oss/niceml/commit/fbb72d4111d806bffb4acaebe1a6ca43d5c82c33))

## 📥 Pull Request Description

The current version of Altair raised multiple deprecation errors. Therefore, altair is updated with
  this PR.

## 👀 Affected Areas

Dashboard

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run


## v0.13.0 (2024-01-16)

### Bug Fixes

- Changed tf-macos version to <=2.14
  ([`a84c6c4`](https://github.com/codecentric-oss/niceml/commit/a84c6c48d2626983f4ed934fa23d596c14c18127))

- Changed tf-macos version to <=2.14
  ([`5516531`](https://github.com/codecentric-oss/niceml/commit/55165313b6a5757f1e60d1dd39761bf4c6002d60))

- **ci**: Set Python version to 3.11 due to an interpretation error of the Github actions
  ([`29bafbf`](https://github.com/codecentric-oss/niceml/commit/29bafbfb5c939292958a4428f7bf5d22e1382ae8))

### Continuous Integration

- **release**: Sets the Python version of the release workflow to 3.10
  ([`8e15200`](https://github.com/codecentric-oss/niceml/commit/8e15200fdcd94c7435d77e90b2a25dcadf720ac6))

- **test**: Add workflow trigger `pull_request_target` to execute the workflow even with fork pull
  requests ([#108](https://github.com/codecentric-oss/niceml/pull/108),
  [`9ae27f9`](https://github.com/codecentric-oss/niceml/commit/9ae27f9932ee55894f4bbce8bd279df4d891835c))

## 📥 Pull Request Description

The following changes and fixes are part of this pull request: - ci(test): Set pipeline trigger to
  `pull_request_target` to execute the pipeline even with fork pull requests - docs: Remove python
  3.8 from Getting Started - refactor: Remove python from classifiers in `pyproject.toml` -
  ci(test): Add workflow trigger `pull_request` back into project

## 👀 Affected Areas

- pytest workflow - docs

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [X] All tests ran successfully - [X] All merge conflicts are
  resolved - [X] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

## 📌 Related Issues

- closes #107

- **test**: Add workflow trigger `pull_request_target` to execute the workflow even with fork pull
  requests ([#108](https://github.com/codecentric-oss/niceml/pull/108),
  [`6a89c5f`](https://github.com/codecentric-oss/niceml/commit/6a89c5f87363e80726a75b0da6845d192a639ed8))

## 📥 Pull Request Description

The following changes and fixes are part of this pull request: - ci(test): Set pipeline trigger to
  `pull_request_target` to execute the pipeline even with fork pull requests - docs: Remove python
  3.8 from Getting Started - refactor: Remove python from classifiers in `pyproject.toml` -
  ci(test): Add workflow trigger `pull_request` back into project

## 👀 Affected Areas

- pytest workflow - docs

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [X] All tests ran successfully - [X] All merge conflicts are
  resolved - [X] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

## 📌 Related Issues

- closes #107

### Features

- Update tensorflow (`>=2.13,<=2.15`) and dagster (`~1.6.0`). Remove support for python `3.8`
  ([#106](https://github.com/codecentric-oss/niceml/pull/106),
  [`71d82cc`](https://github.com/codecentric-oss/niceml/commit/71d82cce48042271d49eecf54813ffdbe53b4dc6))

## 📥 Pull Request Description

- Updated Dagster to Version 1.5 in order to leverage bug fixes in dagster webservice - Fix keras
  import error in order to enable usage of tensorflow 2.15

## 👀 Affected Areas

- Dagster Pipelines & Webservice - Tensorflow ML Backend

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [X] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [ ] All tests ran successfully - [X] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [X] Any necessary
  migrations have been run

## 📌 Related Issues

If this pull request is related to an existing issue, please reference it here.

## 🔗 Links

Please provide any relevant links (e.g. documentation, external resources) that support your
  changes.

## 📷 Screenshots

If applicable, please include screenshots of the before and after effects of your changes.

Thank you for your contribution! 🎉

---------

Co-authored-by: Timo Schadt <timo.schadt@alcon.com>

- Update tensorflow (`>=2.13,<=2.15`) and dagster (`~1.6.0`). Remove support for python `3.8`
  ([#106](https://github.com/codecentric-oss/niceml/pull/106),
  [`9c3f6af`](https://github.com/codecentric-oss/niceml/commit/9c3f6af92059f890c9d5f8bebe4eae55966f16c2))

## 📥 Pull Request Description

- Updated Dagster to Version 1.5 in order to leverage bug fixes in dagster webservice - Fix keras
  import error in order to enable usage of tensorflow 2.15

## 👀 Affected Areas

- Dagster Pipelines & Webservice - Tensorflow ML Backend

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [X] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [ ] All tests ran successfully - [X] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [X] Any necessary
  migrations have been run

## 📌 Related Issues

If this pull request is related to an existing issue, please reference it here.

## 🔗 Links

Please provide any relevant links (e.g. documentation, external resources) that support your
  changes.

## 📷 Screenshots

If applicable, please include screenshots of the before and after effects of your changes.

Thank you for your contribution! 🎉

---------

Co-authored-by: Timo Schadt <timo.schadt@alcon.com>


## v0.12.0 (2024-01-04)

### Bug Fixes

- **Dependencies**: Set `tensorflow-io-gcs-filesystem` to `~0.33.0`
  ([`59a059f`](https://github.com/codecentric-oss/niceml/commit/59a059f9d2e27058779ca1630bdbdbe80bfc8f61))

### Documentation

- Adjust python version information in documentation
  ([`5ea5e93`](https://github.com/codecentric-oss/niceml/commit/5ea5e930244ff187a2acd73704908b19b1250475))

### Features

- **Dependencies**: Allow Python 3.11 and adapt dependency versions
  ([`a60a420`](https://github.com/codecentric-oss/niceml/commit/a60a420803e4a806c15e95d0a004a821aa0489a4))

Add python 3.11 to the test matrix in test workflow


## v0.11.0 (2023-12-20)

### Bug Fixes

- Rename tensorflow to keras
  ([`f38536f`](https://github.com/codecentric-oss/niceml/commit/f38536f802052ca50c60ec4c29d53923913a685c))

### Documentation

- Add `Commit Guidelines `
  ([`c404b38`](https://github.com/codecentric-oss/niceml/commit/c404b383bf7df66cd841d9fae10a5d75300f36d0))

- Add `Developer Environment Setup Guide`
  ([`94d5e83`](https://github.com/codecentric-oss/niceml/commit/94d5e836f8076dfe3e1d048f8e393ddb8c5e1496))

- Add coding standards and contribution guidelines
  ([`3a64c22`](https://github.com/codecentric-oss/niceml/commit/3a64c22d67f4c072c9ac5e6ab27d26d4b156595f))

- Add contribution guidelines and community standards into documentation
  ([`b209c4b`](https://github.com/codecentric-oss/niceml/commit/b209c4b24c6b732060960fca3abecb7f4e662984))

- Optimize coding standards
  ([`3810dcb`](https://github.com/codecentric-oss/niceml/commit/3810dcb24c1e9f612829e541369f96c17568db0d))

- Standardize headings
  ([`50805f7`](https://github.com/codecentric-oss/niceml/commit/50805f7b1251adbe5fea95ea34ac4cfa0676ec3b))

- Update contact information in `CODE_OF_CONDUCT`
  ([`9780565`](https://github.com/codecentric-oss/niceml/commit/978056505747f7beb1d459701cf20b8024d8a409))

- **contribution**: Add information about how conventional and non-conventional commits are handled
  in pull requests
  ([`ec12c19`](https://github.com/codecentric-oss/niceml/commit/ec12c19cef99d53396b2400622a8a853f5a73020))

- **DevEntSetup**: Refactor hint for other than conda
  ([`bc5acfe`](https://github.com/codecentric-oss/niceml/commit/bc5acfe247eb2224224f24c30b07162fad17019b))

- **DevEnvSetup**: Add hint for pipenv or other comparable solutions. Add recommendation for Apple
  Silicon
  ([`2c732f5`](https://github.com/codecentric-oss/niceml/commit/2c732f523874e4f7e800c33c685f1d8a0f3862b2))

### Features

- Add contribution guidelines to the project
  ([#103](https://github.com/codecentric-oss/niceml/pull/103),
  [`b9ea55a`](https://github.com/codecentric-oss/niceml/commit/b9ea55af87908f6c75507aaf6930489fa3f2e20a))

## 📥 Pull Request Description

- docs: Add coding standards and contribution guidelines - docs: Standardize headings - docs: add
  `Developer Environment Setup Guide` - docs: add `Commit Guidelines ` - docs: add contribution
  guidelines and community standards into documentation - docs: Update contact information in
  `CODE_OF_CONDUCT` - docs(DevEnvSetup): Add hint for pipenv or other comparable solutions. Add
  recommendation for Apple Silicon - docs(DevEntSetup): Refactor hint for other than conda -
  docs(contribution): Add information about how conventional and non-conventional commits are
  handled in pull requests

## 👀 Affected Areas

- Repository core files like `CONTRIBUTION.md` - docs

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [X] All tests ran successfully - [X] All merge conflicts are
  resolved - [X] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

- Change model custom objects and callbacks refactored
  ([`c6f9fd3`](https://github.com/codecentric-oss/niceml/commit/c6f9fd39d592559e8656eb07a1bff8d9816c16fa))

- **MLflow**: Allow logging of nested tuple or int metrics in the `TensorGraphAnalyzer`
  ([`daea28a`](https://github.com/codecentric-oss/niceml/commit/daea28a7d76e441d238a044b2973ccf57a27e35e))

Adjust and extend unit test cases for `metrics_dict_to_mlflow_metrics_dict`


## v0.10.0 (2023-12-12)

### Features

- Optimize file locks ([#94](https://github.com/codecentric-oss/niceml/pull/94),
  [`907c169`](https://github.com/codecentric-oss/niceml/commit/907c169c257c30a158b32b9c15359bb1ed8100ec))

## 📥 Pull Request Description

Optimize FileLocks and add tests

## 👀 Affected Areas

All occurencies of the File locks and testing.

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run


## v0.9.1 (2023-12-05)

### Bug Fixes

- List_dir filter_ext ([#93](https://github.com/codecentric-oss/niceml/pull/93),
  [`d8171fb`](https://github.com/codecentric-oss/niceml/commit/d8171fb2dfd5c7620767e3b409263def521b8423))

## 📥 Pull Request Description

The filter_ext filtering was performed before the files in the subfolders were extracted (recursive
  logic). This led to Bug #91 .

## 👀 Affected Areas

Every list_dir, where the filter_ext is used.

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

---------

Co-authored-by: Denis Stalz-John <denis.stalz-john@codecentric.de>

Co-authored-by: Nils Uhrberg <nils.uhrberg@codecentric.de>


## v0.9.0 (2023-11-28)

### Bug Fixes

- Pillow vulnerability and other + formatting
  ([#89](https://github.com/codecentric-oss/niceml/pull/89),
  [`3d3e6af`](https://github.com/codecentric-oss/niceml/commit/3d3e6af88b2d353c136aec8ba7a825d899673087))

## 📥 Pull Request Description

Fix vulnerabilities and run some pre-commit hooks for reformatting etc...

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed (not all green) - [x] Changes have been reviewed by at least
  one other developer - [ ] Tests have been added or updated to cover the changes (only necessary if
  the changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts
  are resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

---------

Co-authored-by: Nils <nils.uhrberg@codecentric.de>

- Pillow vulnerability and other + formatting
  ([#89](https://github.com/codecentric-oss/niceml/pull/89),
  [`9c62f3b`](https://github.com/codecentric-oss/niceml/commit/9c62f3b29b686b4d5c21bb46805a719b8a632c12))

## 📥 Pull Request Description

Fix vulnerabilities and run some pre-commit hooks for reformatting etc...

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed (not all green) - [x] Changes have been reviewed by at least
  one other developer - [ ] Tests have been added or updated to cover the changes (only necessary if
  the changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts
  are resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

---------

Co-authored-by: Nils <nils.uhrberg@codecentric.de>

### Features

- Write and read json options in experiment context
  ([#90](https://github.com/codecentric-oss/niceml/pull/90),
  [`77d3dc9`](https://github.com/codecentric-oss/niceml/commit/77d3dc92b71087f3787ff6d51d5761f73e52c2a3))

## 📥 Pull Request Description

Added write and read options for json files to ExperimentContext. This enables the user to write out
  additional Information, for example target classes.

## 👀 Affected Areas

Trainings Pipelines

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

- Write and read json options in experiment context
  ([#90](https://github.com/codecentric-oss/niceml/pull/90),
  [`1aa8bd5`](https://github.com/codecentric-oss/niceml/commit/1aa8bd537ed127ac299209e5d478bc5389650a91))

## 📥 Pull Request Description

Added write and read options for json files to ExperimentContext. This enables the user to write out
  additional Information, for example target classes.

## 👀 Affected Areas

Trainings Pipelines

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run


## v0.8.3 (2023-11-08)

### Bug Fixes

- Generate mkdocs graphs with multiple dependencies
  ([#86](https://github.com/codecentric-oss/niceml/pull/86),
  [`ac56427`](https://github.com/codecentric-oss/niceml/commit/ac564270c8b1ea0cb3d8f7fa86ee0ceac639b4fc))

## 📥 Pull Request Description

Implemented option to generate pipeline graphs of dagster jobs with multiple op dependencies.

## 👀 Affected Areas

Documentation

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

- Generate mkdocs graphs with multiple dependencies
  ([#86](https://github.com/codecentric-oss/niceml/pull/86),
  [`61488b2`](https://github.com/codecentric-oss/niceml/commit/61488b29cde38ecabda9c60188150724409ca757))

## 📥 Pull Request Description

Implemented option to generate pipeline graphs of dagster jobs with multiple op dependencies.

## 👀 Affected Areas

Documentation

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

- Reload finished experiments in dashboard
  ([#87](https://github.com/codecentric-oss/niceml/pull/87),
  [`39764f5`](https://github.com/codecentric-oss/niceml/commit/39764f5238696881e1002e2a3b6e454457efe4c9))

## 📥 Pull Request Description

If the dashboard was started during a running experiment, the experiment was visible in the
  dashboard but with incomplete information. Even after the experiment was finished, the Cache was
  not updated, so the experiment would still be incomplete in the dashboard.

This issue was fixed by checking for the latest modification in the experiment files and updating
  the cache, if it was outdated.

Additionaly, the test pipeline was fixed, by defining the execution sequence of tests.

## 👀 Affected Areas

- dashboard - test pipeline

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

---------

Co-authored-by: Denis Stalz-John <denis.stalz-john@codecentric.de>

- Reload finished experiments in dashboard
  ([#87](https://github.com/codecentric-oss/niceml/pull/87),
  [`aafe59a`](https://github.com/codecentric-oss/niceml/commit/aafe59a160dd73d84697ddfa0ff26447139c32f5))

## 📥 Pull Request Description

If the dashboard was started during a running experiment, the experiment was visible in the
  dashboard but with incomplete information. Even after the experiment was finished, the Cache was
  not updated, so the experiment would still be incomplete in the dashboard.

This issue was fixed by checking for the latest modification in the experiment files and updating
  the cache, if it was outdated.

Additionaly, the test pipeline was fixed, by defining the execution sequence of tests.

## 👀 Affected Areas

- dashboard - test pipeline

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

---------

Co-authored-by: Denis Stalz-John <denis.stalz-john@codecentric.de>

- Replace lambda `class_extractor` in `DirClsDataInfoListing` with a private function because
  lambdas are not pickable ([#85](https://github.com/codecentric-oss/niceml/pull/85),
  [`def7d1a`](https://github.com/codecentric-oss/niceml/commit/def7d1ae08168ce2edef063268b9ae95b9c60f18))

## 📥 Pull Request Description

Replace lambda `class_extractor` in `DirClsDataInfoListing` with a private function because lambdas
  are not pickable

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run


## v0.8.2 (2023-10-09)

### Bug Fixes

- Add installation info to main documentation
  ([`b2f8c10`](https://github.com/codecentric-oss/niceml/commit/b2f8c10f1c0ab4a7e95ac08092f585f2f6a9ba46))

- Add installation info to main documentation
  ([#84](https://github.com/codecentric-oss/niceml/pull/84),
  [`10e60db`](https://github.com/codecentric-oss/niceml/commit/10e60dbc999e2e396a223d2bbc81f4329a807264))

## 📥 Pull Request Description

Added simple installation information to the main documentation page.

## 👀 Affected Areas

Documentation

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [x] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

- Remove job flag to prevent multiple mlflow runs
  ([`8c8b78f`](https://github.com/codecentric-oss/niceml/commit/8c8b78f71dc514abe444b6f6bf125aaf707c38ea))

- Remove job flag to prevent multiple mlflow runs
  ([#82](https://github.com/codecentric-oss/niceml/pull/82),
  [`31b3875`](https://github.com/codecentric-oss/niceml/commit/31b3875cf062d594afe42406fdb9dfeb6586c88e))

## 📥 Pull Request Description

This pull request fixes a bug, which created two experiment runs out of one dagster pipeline run.
  This is a bug, caused by the dagster itegration of MLFlow. The implementation in niceML was
  correct. When the bug of this package is fixed in the future, niceML may has to be updated as
  well. With this fix, niceML, dagster and MLFlow work and only one MLFlow experiment run is created
  per dagster pipeline run.

## 👀 Affected Areas

Dagster Pipeline MLFlow integration

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

- Replace lambda `class_extractor` in `DirClsDataInfoListing` with a private function because
  lambdas are not pickable ([#85](https://github.com/codecentric-oss/niceml/pull/85),
  [`98f25df`](https://github.com/codecentric-oss/niceml/commit/98f25df82a7275260f9588830cae727c2a21c0d5))

## 📥 Pull Request Description

Replace lambda `class_extractor` in `DirClsDataInfoListing` with a private function because lambdas
  are not pickable

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run


## v0.8.1 (2023-09-26)

### Bug Fixes

- Analysis now have credentials for datasets
  ([#81](https://github.com/codecentric-oss/niceml/pull/81),
  [`aeb6e63`](https://github.com/codecentric-oss/niceml/commit/aeb6e63846004a97c069d5849fb8fb34657d65d2))

## 📥 Pull Request Description

Fixed a bug that in the analysis step the credentials for the datasets were not available.

## 👀 Affected Areas

pipelines, code

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

Thank you for your contribution! 🎉


## v0.8.0 (2023-09-21)

### Bug Fixes

- Analysis now have credentials for datasets
  ([`87f7214`](https://github.com/codecentric-oss/niceml/commit/87f72148dbadab64370bb84004d8242127c1a558))

- Return the experiment path instead of the `ExperimentInfo` if `exp_id` is not latest
  ([#76](https://github.com/codecentric-oss/niceml/pull/76),
  [`2d31041`](https://github.com/codecentric-oss/niceml/commit/2d310411d94aae32e8410b4b0299fc4b06620a4f))

## 📥 Pull Request Description

There was a bug that the `get_exp_filepath` function returns an`ExperimentInfo` instead of the
  experiment file path if the exp_id is something else than "latest". This is fixed with this pull
  request.

## 👀 Affected Areas

- eval pipeline --> load experiment

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

### Continuous Integration

- Copy config files to the template as part of the release workflow
  ([#77](https://github.com/codecentric-oss/niceml/pull/77),
  [`de9605e`](https://github.com/codecentric-oss/niceml/commit/de9605ef44b7a19239e4a50760d036417240395b))

## 📥 Pull Request Description

This pr fixes #75. As part of the release workflow, the project's configuration files are copied to
  the template folder

## 👀 Affected Areas

- project template - release workflow

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [x] Any necessary
  migrations have been run

### Features

- Add predictionfunction and models as folder
  ([#78](https://github.com/codecentric-oss/niceml/pull/78),
  [`368c25c`](https://github.com/codecentric-oss/niceml/commit/368c25c18b3a2de3b82119fb74b7c3f3a4bd53ec))

## 📥 Pull Request Description

Allow models to be folders or files. Create a prediction function which handles different prediction
  model types.

## 👀 Affected Areas

- documentation - configuration - implementation

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [ ] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

- Integrate mlflow in niceml ([#79](https://github.com/codecentric-oss/niceml/pull/79),
  [`23aa7dc`](https://github.com/codecentric-oss/niceml/commit/23aa7dce5de354d00c674e61099522ee4cfda668))

## 📥 Pull Request Description

Integrated mlflow in the train and eval job.

## 👀 Affected Areas

Affects code and tests.

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [X] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [X] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

---------

Co-authored-by: Nils <nils.uhrberg@codecentric.de>


## v0.7.3 (2023-09-04)


## v0.7.2 (2023-09-01)

### Bug Fixes

- Implemented image_size.from_pil image and size
  ([#71](https://github.com/codecentric-oss/niceml/pull/71),
  [`0643bf2`](https://github.com/codecentric-oss/niceml/commit/0643bf2c659d3d7d82c4bc9b6a9b46c8ba934e3c))

## 📥 Pull Request Description

Now it is possible to create an ImageSize from an PIL image and also its size.

## 👀 Affected Areas

tests, imagesize

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [x] Any necessary
  migrations have been run

Co-authored-by: Nils <nils.uhrberg@codecentric.de>

- Optimize file locks and remove outdated template config
  ([#72](https://github.com/codecentric-oss/niceml/pull/72),
  [`dc374a6`](https://github.com/codecentric-oss/niceml/commit/dc374a639da2214cea77654e6da3a610f7a31aa5))

## 📥 Pull Request Description

The 'is_acquired' parameter of FileLocks can now be set when the Lock is initialized. This can be
  necessary, if a FileLock file is already present, but the according FileLock object is not. This
  may happen, if a FileLock could not have been released e.g. due to an error.

Additionally, an outdated config was removed from a template configuration.

## 👀 Affected Areas

Everywhere a FileLock is used.

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

- Remove `tensorflow-io-gcs-filesystem` as a dependency from the project template
  ([`ce4ea6c`](https://github.com/codecentric-oss/niceml/commit/ce4ea6c142cee8ecd611cc80a64863202bed3749))

- Remove Windows as an option in `niceml init`.
  ([`a07cab4`](https://github.com/codecentric-oss/niceml/commit/a07cab4e641a1d9caf3b8f9b246382b397ed29d9))

- Remove Windows from documentation
  ([`0c252aa`](https://github.com/codecentric-oss/niceml/commit/0c252aa9e779f42233a810dd242d8934c3edeec9))

- Safely remove `tensorflow-io-gcs-filesystem` from `poetry-lock`
  ([`31515ca`](https://github.com/codecentric-oss/niceml/commit/31515cadd8c6c1eacaf2000cc6e7e135a4b73257))


## v0.7.1 (2023-08-22)

### Bug Fixes

- Remove tensorflow-io-gcs-filesystem from dependencies
  ([#69](https://github.com/codecentric-oss/niceml/pull/69),
  [`cfbadc8`](https://github.com/codecentric-oss/niceml/commit/cfbadc850e295a69f604a5431c98627fd66ae938))

## 📥 Pull Request Description

Even though tensorflow-io-gcs-filesystem was declared as optional poetry tried to install it when
  installing tensorflow-macos. That is why we removed the unnecessary package.

## 👀 Affected Areas

Installation and dependencies.

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [ ] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [ ] Any necessary
  migrations have been run

---------

Co-authored-by: Nils Uhrberg <nils.uhrberg@codecentric.de>


## v0.7.0 (2023-08-15)


## v0.6.1 (2023-08-02)

### Bug Fixes

- Change type of `image_path` in `load_img_uint8`
  ([#55](https://github.com/codecentric-oss/niceml/pull/55),
  [`7df85ee`](https://github.com/codecentric-oss/niceml/commit/7df85ee5ba3980a8b90e267e5a0b6f56c3254ef5))

## 📥 Pull Request Description

load_img_uint8 did not work if image_path is not str but LocationConfig type.

## 👀 Affected Areas

imageloading.py

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [x] Documentation has been updated to reflect the changes - [x] Any necessary
  migrations have been run

- How to guide one yaml was false indented
  ([`61c023c`](https://github.com/codecentric-oss/niceml/commit/61c023c123e5fe153613f2b5b6505d73e940c470))

- Pr feedback
  ([`bd6d475`](https://github.com/codecentric-oss/niceml/commit/bd6d475514ca1fa0a8538283da9b2ec52590aa3a))

- Pr feedback
  ([`c76a6e6`](https://github.com/codecentric-oss/niceml/commit/c76a6e6292d6d21e616043fd91d392cdfa72e9bb))

- Set `pydantic` version to `<2.0`
  ([`6b63ef1`](https://github.com/codecentric-oss/niceml/commit/6b63ef1b2b57653822419d26a71c89569a65a2cc))

- Solve niceML installation issue due to pydantic and dagster version missmatsch(#57)
  ([`9303e19`](https://github.com/codecentric-oss/niceml/commit/9303e19f8f5080a93030f89a2b560dc081efc191))

## 📥 Pull Request Description

The currently used version of `dagster` (`1.3.9`) does not work with the latest version of
  `pydantic` (`2.x`). Due to this issue, it is necessary to set the maximum allowed version of
  `pydantic` to `<2.0` until dagster fixes the problem.

Also, some security holes have been closed.

## 👀 Affected Areas

- project dependencies - ## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [X] All tests ran successfully - [X] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [X] Any necessary
  migrations have been run

## 📌 Related Issues

_None_

## 🔗 Links

## 📷 Screenshots

- Update `cryptrography` to ^41.0.0
  ([`b188f99`](https://github.com/codecentric-oss/niceml/commit/b188f9913ad94c3045957d4dc0928d26d3fdd225))

- Update `dagster` to ~1.3.13
  ([`c842df0`](https://github.com/codecentric-oss/niceml/commit/c842df0dd2a01084438108a14ab509439772ff8f))

- Update `requests` to ^2.13.0
  ([`6559b64`](https://github.com/codecentric-oss/niceml/commit/6559b6466ea56bd204ad468c8fb65d0db8257e55))

- Update `tornado` to ^6.3.2
  ([`6315889`](https://github.com/codecentric-oss/niceml/commit/6315889213a422f6b27d75195d97e2d50017be69))

### Code Style

- Improved waittime messages for locks ([#64](https://github.com/codecentric-oss/niceml/pull/64),
  [`a08e76b`](https://github.com/codecentric-oss/niceml/commit/a08e76b015ebe50bf378c8c1a34f84b3e6b141fd))

## 📥 Pull Request Description

Give wait time information while waiting on file lock release.

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [x] Documentation has been updated to reflect the changes - [x] Any necessary
  migrations have been run

- **docu**: Add link how to add pycharm config for debugging
  ([`bbbd60d`](https://github.com/codecentric-oss/niceml/commit/bbbd60dfbf8f5fb03e9a9bc23127a9b1321f237e))

- **docu**: Remove typos
  ([`fa0a301`](https://github.com/codecentric-oss/niceml/commit/fa0a301625c657262ebb4eab40468263e334160a))

### Documentation

- Add automatic generation of API documentation based on docstrings
  ([#54](https://github.com/codecentric-oss/niceml/pull/54),
  [`8a16e6f`](https://github.com/codecentric-oss/niceml/commit/8a16e6ffe9c80a446766721e078f869c256ed1fd))

## 📥 Pull Request Description

API documentation is automatically generated based on the docstrings of a package, module, class,
  function, and method. The navigation structure is generated based on the package structure of
  niceML.

## 👀 Affected Areas

- docs - **DOCS NAVIGATION** - The navigation entries are now created via the file
  `docs/SUMMARY.md`.

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [X] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [X] All tests ran successfully - [X] All merge conflicts are
  resolved - [X] Documentation has been updated to reflect the changes - [X] Any necessary
  migrations have been run

## 📌 Related Issues

*None*

## 🔗 Links

## 📷 Screenshots

**Example API doc entry**

<img width="1451" alt="Bildschirmfoto 2023-07-20 um 15 48 32"
  src="https://github.com/codecentric-oss/niceml/assets/48205130/c4d76df3-38a2-4147-ad11-30bebcac7d1e">

- Add how to add a custom model
  ([`4027ef8`](https://github.com/codecentric-oss/niceml/commit/4027ef8727bbca24370aa703b26873618d4e627f))

- Add how to start the pipeline via dagster-webserver
  ([`79a4db0`](https://github.com/codecentric-oss/niceml/commit/79a4db0014ce684fcec4d23ea923f02de52688ef))

- Add how to write a custom pipeline
  ([`66fe21c`](https://github.com/codecentric-oss/niceml/commit/66fe21c58fc60d5a355544ebb561a0e9612e9e59))

- Add into to how to write a custom pipeline
  ([`f0ec339`](https://github.com/codecentric-oss/niceml/commit/f0ec3395729a7362b0fc90754b4f000cbe37b50f))

- Add PR feedback
  ([`84b6c6c`](https://github.com/codecentric-oss/niceml/commit/84b6c6ce2a11bc29a6431b8ebd8f16aa353bb332))

### Features

- Improvements to `DfDataset` and other files to better perform regression experiments
  ([#56](https://github.com/codecentric-oss/niceml/pull/56),
  [`f88abd8`](https://github.com/codecentric-oss/niceml/commit/f88abd8083a8202a4354f30e268b55a33037d9f4))

## 📥 Pull Request Description

This pull request includes changes that specifically affect the 'DfDataset' or working with
  structured data. This includes the following functions and corrections:

- feat: Load data (parquet) directly when initializing a `DfDataset` - feat: Add some functions from
  the `GenericDataset` (`get_set_name`, `get_batch_size`) - fix: Add ZeroDevisionError into
  dataframe normalization - fix: Optimize performance of `get_datainfo` - feat: Add `__getattr__`
  into `RegDataInfo` - feat: Add denormalization for dataframe columns - feat: Add `FeatureTypes`
  for dataframe normalization - feat: Add normalization functions and `NormalizationInfo`s for
  scalar, categorical, and binary feature columns - fix: Handling of columns with equal values
  during normalization - feat: Add `FeatureCombiner` as part of the DfDataset - fix: Remove
  deprecated `pandas.append` from `CSVLogger` - fix: Remove superfluous `RemoteDiskDfLoader` - feat:
  Use numbers tabular data for regression example

## 👀 Affected Areas

- `DfDataset` - `DfLoader` - Dataframe normalization - Tests

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [X] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [ ] All tests ran successfully - [X] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [X] Any necessary
  migrations have been run

## 📌 Related Issues

_None_

## 🔗 Links

## 📷 Screenshots

---------

Co-authored-by: Denis Stalz-John <denis.stalz-john@codecentric.de>

- Join location with path objects ([#63](https://github.com/codecentric-oss/niceml/pull/63),
  [`d73286d`](https://github.com/codecentric-oss/niceml/commit/d73286d5980dda3048025a1f2508650b794de796))

## 📥 Pull Request Description

'join_location_w_path' now accepts a list of path objects, which will be joined to the location.
  This way, one can now join a location with a subfolder and its file in one step instead of having
  to call the function multiple times. The original functionality remains intact.

## 👀 Affected Areas

All areas where a location is joined with a path can now profit from the change.

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [x] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [x] All tests ran successfully - [x] All merge conflicts are
  resolved - [x] Documentation has been updated to reflect the changes - [x] Any necessary
  migrations have been run

- **Dependencies**: Update of `dagster` to 1.4.x , `tensorflow`, and the corresponding packages to
  2.12.x ([#60](https://github.com/codecentric-oss/niceml/pull/60),
  [`99b997e`](https://github.com/codecentric-oss/niceml/commit/99b997e460033ab97db86375b00deff8f5b77b29))

## 📥 Pull Request Description

Due to various security vulnerabilities and version differences, it makes sense to increase the
  `tensorflow` version. In this course, the `dagster` version is also increased.

The following changes have been made:

- fix: removed decay from RMS prop config - fix: Update requests to 2.31.0 (CVE-2023-32681) - feat:
  Update of `dagster` to 1.4.x , `tensorflow`, and the corresponding packages to 2.12.x

## 👀 Affected Areas

- Project dependencies

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [X] All tests ran successfully - [X] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [X] Any necessary
  migrations have been run

## 📌 Related Issues

Closes #62

## 🔗 Links

_None_

## 📷 Screenshots

---------

Co-authored-by: Denis Stalz-John <denis.stalz-john@codecentric.de>


## v0.6.0 (2023-07-10)

### Bug Fixes

- Adjust supported python versions in `Getting Started` docs section
  ([`4bde794`](https://github.com/codecentric-oss/niceml/commit/4bde794d881d9c1c397d86a61bb040e1f96cbec8))

- Remove temp directory from hydra search path. Add hydra config mapping factory
  ([#47](https://github.com/codecentric-oss/niceml/pull/47),
  [`6660ec9`](https://github.com/codecentric-oss/niceml/commit/6660ec91484c40fb21fdb3335e1244f24d757923))

## 📥 Pull Request Description

Until now, a temporary directory was always added to the search path of a `dagster` configuration.
  This caused `dagster` to give an error message when the configurations had to be searched. The
  temporary directory is necessary for the operation with `dagit`, because no configuration file has
  to be specified there, but directly YAML code. In this pull request the temporary directory was
  removed from the searchpath configuration. Also, there is now a `hydra_conf_mapping_factory` that
  is used as a decorator of a Dagster job, as this allows parameters to be passed and overridden.

## 👀 Affected Areas

- Pipelines

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [X] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [ ] Documentation has been updated to reflect the changes -
  **Not necessary** - [X] Any necessary migrations have been run - Pipelines run via a `dagster`
  script, but can also be started via `dagit`.

## 📌 Related Issues

- closes #42

## 🔗 Links

*None*

## 📷 Screenshots

`dagster` pipeline run

<img width="1586" alt="Bildschirmfoto 2023-07-05 um 08 08 35"
  src="https://github.com/codecentric-oss/niceml/assets/48205130/661a1cf7-7c01-45ed-bbdf-5f87abd9df26">

`dagit` pipeline run

![Capture-2023-07-05-080913](https://github.com/codecentric-oss/niceml/assets/48205130/785da3f9-eaf5-45eb-9bfb-8666317675dd)

- Save result files from `tensorgraphanalyzer` at the correct place and implemented validation for
  that ([#50](https://github.com/codecentric-oss/niceml/pull/50),
  [`ea3191b`](https://github.com/codecentric-oss/niceml/commit/ea3191b3c0fc31d7e435b30a74c16751c939a3b3))

Implemented a fix in the tensorgraphanalyzer to save the result files at the correct location.
  Improved the ExperimentSchemas to recognize such missing or incorrect saved files.

### Features

- Add `NanDataframeFilter` to drop nan values of feature columns
  ([#51](https://github.com/codecentric-oss/niceml/pull/51),
  [`3561200`](https://github.com/codecentric-oss/niceml/commit/3561200187c4073e2aec4631dd54572bd0686a11))

## 📥 Pull Request Description

A `DataframeFilter` is used to filter tabular data in a `DfDataset`. Besides the abstract
  implementation, a `NaNDataframeFilter` has also been implemented, which removes rows with NaN
  values in the input and target columns of the data description.

## 👀 Affected Areas

- `DataframeFilter` (**new**)

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [ ] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [X] All tests ran successfully - [X] All merge conflicts are
  resolved - [ ] Documentation has been updated to reflect the changes - [x] Any necessary
  migrations have been run

## 📌 Related Issues

*None*

## 🔗 Links

_None_

## 📷 Screenshots

- Add dagster op for dataframe normalization
  ([#48](https://github.com/codecentric-oss/niceml/pull/48),
  [`fe0e8e0`](https://github.com/codecentric-oss/niceml/commit/fe0e8e07a3792ae830bddd5cdf904017f67d148b))

## 📥 Pull Request Description

An option has been added to allow the normalization of data frames in a `dagster` pipeline. A list
  of features to be normalized can be specified. Alternatively, a function can be passed that
  returns the feature columns.

## 👀 Affected Areas

- `dagster` pipelines

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [X] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [ ] Documentation has been updated to reflect the changes -
  **Not necessary** - [X] Any necessary migrations have been run

## 📌 Related Issues

*None*

## 🔗 Links

## 📷 Screenshots

- Add lockfile name as attribute of `FileChecksumProcessor `
  ([#46](https://github.com/codecentric-oss/niceml/pull/46),
  [`013addf`](https://github.com/codecentric-oss/niceml/commit/013addfdcf3d23de3c025a1e4c95b7c11fd0a0ac))

## 📥 Pull Request Description

To be more flexible in the configuration of a `FileChecksumProcessor` a lock file name can now be
  specified. The default value is `lock.yaml`.

## 👀 Affected Areas

- `FileChecksumProcessor` and its subclasses

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [x] Changes have been reviewed by at least one other
  developer - [X] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [ ] Documentation has been updated to reflect the changes -
  **Not necessary** - [ ] Any necessary migrations have been run - **Not necessary**

## 📌 Related Issues

*None*

## 🔗 Links

*None* ## 📷 Screenshots


## v0.5.0 (2023-06-23)

### Features

- Add abstract `FileChecksumProcessor` and concrete class `ZippedCsvToParquetProcessor`
  ([#44](https://github.com/codecentric-oss/niceml/pull/44),
  [`a21d673`](https://github.com/codecentric-oss/niceml/commit/a21d67300705f3f1f4fc1515c567adef74ecfec5))

## 📥 Pull Request Description

With a FileChecksumProcessors, files from an input directory can be processed and the results can
  then be saved in an output directory. The checksums of input and output files are created and
  saved so that only files that have changed are processed when executed again.

## 👀 Affected Areas

Core implementation. Mostly part of a sort of data preprocessing pipeline.

## 📝 Checklist

Please make sure you've completed the following tasks before submitting this pull request:

- [X] Pre-commit hooks were executed - [ ] Changes have been reviewed by at least one other
  developer - [X] Tests have been added or updated to cover the changes (only necessary if the
  changes affect the executable code) - [ ] Documentation has been updated to reflect the changes -
  [X] Any necessary migrations have been run

## 📌 Related Issues

*None*

## 🔗 Links

## 📷 Screenshots

---------

Co-authored-by: Denis Stalz-John <denis.stalz-john@codecentric.de>

- Implementation of filelocks ([#43](https://github.com/codecentric-oss/niceml/pull/43),
  [`9d4dacd`](https://github.com/codecentric-oss/niceml/commit/9d4dacd7e9b09a764f45fdf2dc1c5c701dc19535))

Implemented read and writelocks for training and evaluation jobs.


## v0.4.1 (2023-06-22)

### Bug Fixes

- Added protobuf version ([#32](https://github.com/codecentric-oss/niceml/pull/32),
  [`1ce7e8f`](https://github.com/codecentric-oss/niceml/commit/1ce7e8f2c25d7ba9035ad13ab7df6753e9746497))

Added protobuf version for tf-macos

Co-authored-by: Nils Uhrberg <nils.uhrberg@codecentric.de>

- Update the version of dagster to 1.3.9 ([#34](https://github.com/codecentric-oss/niceml/pull/34),
  [`118643d`](https://github.com/codecentric-oss/niceml/commit/118643d5742d189ba414d34080897390939cfd24))

To close a vulnerability in `sqlalchemy` the version of `dagster` was updated to `1.3.9`. Fix #33


## v0.4.0 (2023-06-05)

### Features

- New tensorflow-metal version
  ([`e629895`](https://github.com/codecentric-oss/niceml/commit/e629895a8012edb7520c6d816e1dc961a46b621d))

- New tensorflow-metal version ([#29](https://github.com/codecentric-oss/niceml/pull/29),
  [`721842b`](https://github.com/codecentric-oss/niceml/commit/721842b2f656fe200634290015dad721aab05a61))

added new tensorflow metal version

- Softmax for Semantic Segmentation ([#30](https://github.com/codecentric-oss/niceml/pull/30),
  [`ec669b1`](https://github.com/codecentric-oss/niceml/commit/ec669b1bd9cf1c8e355707fcec75d3e1dcb50bde))

Add option to use a softmax for Semantic Segmentation - implement void/background class - adjust
  SemSegFocalLoss to correct alpha with void/background class


## v0.3.0 (2023-05-17)

### Bug Fixes

- Add default arguments to cli commands where reasonable
  ([`1727959`](https://github.com/codecentric-oss/niceml/commit/17279597b2888b3aea85d0983c7b26712c404393))

- Adjust explanatory comments for albumentation
  ([`6f35f88`](https://github.com/codecentric-oss/niceml/commit/6f35f882645ca1e11d0815dba9fd1b5b13a0c94d))

- Adjust the tests for image generation for albumentation
  ([`6db814c`](https://github.com/codecentric-oss/niceml/commit/6db814cf157657cbddee172b78d966dfd64d1345))

- Allow `None` as initial value for generating number images
  ([`55272e5`](https://github.com/codecentric-oss/niceml/commit/55272e55ec26cafddbed69172188c0a0779bda56))

- Improvements that for eacht subset a row is written
  ([`5982ae3`](https://github.com/codecentric-oss/niceml/commit/5982ae3a715410ea1b354bd3891aefd7840c309f))

- Make all env variables work by default
  ([`9b25b78`](https://github.com/codecentric-oss/niceml/commit/9b25b78d69546f18a09e011b2a5fd3b56c4226c9))

- Make all template env variables work by default
  ([`e7b7019`](https://github.com/codecentric-oss/niceml/commit/e7b70193aed4d5d5b6bd23dfc82e3155fbb0f955))

- Replace environment variable `OUTPUT_PATH` by `EXPERIMENT_URI`
  ([`d98858c`](https://github.com/codecentric-oss/niceml/commit/d98858c0fbd82fa66761a88aa06f58f730cb5e55))

- Replace weak md5 hash (CWE-327)
  ([`a438cc9`](https://github.com/codecentric-oss/niceml/commit/a438cc932830e39f04666486c2276d5cca57c679))

- Transfer default for experiment_uri to files
  ([`1986cd6`](https://github.com/codecentric-oss/niceml/commit/1986cd64586cee07d6ab757175a304230dcab2cf))

- Update `dagster` and add `dagit` (1.3.3)
  ([`66e4c9f`](https://github.com/codecentric-oss/niceml/commit/66e4c9f678a0b0f7adc3267c8cecff9b3596ab32))

### Features

- Add albumentation for numbers dataset image augmentation
  ([`8da7b24`](https://github.com/codecentric-oss/niceml/commit/8da7b248bc6691c05da54758aae4974f39ff9fe8))

- Add conversion of cropped_numbers_images to tabular data as an op
  ([`28bfafc`](https://github.com/codecentric-oss/niceml/commit/28bfafc58d53ac766a318056a751ab1b461d79fd))


## v0.2.0 (2023-05-10)

### Bug Fixes

- Resize bg_images in assets for smaller wheel size
  ([#11](https://github.com/codecentric-oss/niceml/pull/11),
  [`da291f4`](https://github.com/codecentric-oss/niceml/commit/da291f4c230fa5a186f441432596e26eac4460fb))

- resize background images for data generation to smaller wheel size - add conceptual documentation

---------

Co-authored-by: Nils Uhrberg <nils.uhrberg@codecentric.de>

### Features

- Add `niceml init` as cli command to initialize a new niceml project
  ([#13](https://github.com/codecentric-oss/niceml/pull/13),
  [`4f3090a`](https://github.com/codecentric-oss/niceml/commit/4f3090acbc68db2d63f3d42ce7a20aa64f229643))

- Add copier template - Add copier script - Add cli command `init`

---------

Co-authored-by: Nils Uhrberg <nils.uhrberg@codecentric.de>


## v0.1.1 (2023-04-28)
