# CHANGELOG

## v0.17.0-dev.1 (2024-08-07)

### Feature

* feat: Add possibility to pass additional arguments when initializing a `ResultAnalyzer` (#134)

## 📥 Pull Request Description

This PR adds the following features and changes:

- feat: Add possibility to pass additional arguments when initializing a
`ResultAnalyzer`
- refactor: Add an experiment context to the `initialize` function of
the `DataframeAnalyzer`
- refactor: Pass the experiment context of a train or eval pipeline run
to the result analyzer.

## 👀 Affected Areas

- Result analyzers
- Analyse op 
- Train and eval job ([`6e48893`](https://github.com/codecentric-oss/niceml/commit/6e48893b6734a554eacaf30985926dd865f8a275))

## v0.16.1-dev.1 (2024-07-23)

### Ci

* ci: Adjust version_variables and version_toml for semantic-release (#133)

## 📥 Pull Request Description

- Replace version_variable by version_variables and version_toml

## 👀 Affected Areas

- pyproject.toml
- CI/CD ([`3bf6d0e`](https://github.com/codecentric-oss/niceml/commit/3bf6d0e5a9cd30642f26a8f6226959df484283c4))

* ci: update used python version in docs pipeline ([`f6258a1`](https://github.com/codecentric-oss/niceml/commit/f6258a179b61ce0cd44944e001ed1387c840b3f2))

* ci: fix prerelease flag in pre-release pipeline ([`f5fb645`](https://github.com/codecentric-oss/niceml/commit/f5fb6451d97b74045fd7b356bc6dea64f77ba14b))

* ci: Update python-semantic-release and add pre-release pipeline for dev branch ([`16a28c1`](https://github.com/codecentric-oss/niceml/commit/16a28c14efbce9114d7a3a6741b067116e849166))

### Fix

* fix: Downgrade `python-semantic-release` and adjust build command (#132) ([`b23fce4`](https://github.com/codecentric-oss/niceml/commit/b23fce47ad25de30964a532e79c25638b9f41cb9))

* fix: change version (#130)

## 📥 Pull Request Description

Please describe your changes in detail and provide any necessary
context.

## 👀 Affected Areas

Please indicate which areas of the project are affected by your changes
(e.g. dashboard, pipelines, tests, documentation).

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [ ] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`7343560`](https://github.com/codecentric-oss/niceml/commit/7343560dcaf30bb29334348ed4387c6dc0f5361d))

### Refactor

* refactor: Allow `kwargs` in `write_image` ([`f1c13f0`](https://github.com/codecentric-oss/niceml/commit/f1c13f051e92dbed379b325f7032f420de997305))

* refactor: Update dependencies ([`485983b`](https://github.com/codecentric-oss/niceml/commit/485983b5a8dbfa8d12dc55765e7705fcb4682964))

### Unknown

* Merge branch &#39;main&#39; into develop ([`7c04b92`](https://github.com/codecentric-oss/niceml/commit/7c04b92bb8c1579e0d7fd82d03608d7ab942ce7f))

* Pre-Release and new versioning (#129)

## 📥 Pull Request Description

Please describe your changes in detail and provide any necessary
context.

## 👀 Affected Areas

Please indicate which areas of the project are affected by your changes
(e.g. dashboard, pipelines, tests, documentation).

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [ ] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`f237a49`](https://github.com/codecentric-oss/niceml/commit/f237a4948ecd4a64a16e3a8734a0d442d94805c8))

* Feature/versioning with ge (#128)

## 📥 Pull Request Description

Changed all possible versions to &gt;=


## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`2713f33`](https://github.com/codecentric-oss/niceml/commit/2713f33777a5f63b2ff718aec732f681760c6fea))

## v0.16.0 (2024-06-13)

### Feature

* feat: add file loader ([`ea916b7`](https://github.com/codecentric-oss/niceml/commit/ea916b7edba9fbfa4b39c46e3c283aadd187c35a))

### Fix

* fix: localizeexperiment with location config ([`5edff9f`](https://github.com/codecentric-oss/niceml/commit/5edff9ff27c42b8558fbf3d640cbc689d58330b1))

## v0.15.0 (2024-05-15)

### Feature

* feat: allow freeze of model weights in training

## 📥 Pull Request Description

The following changes, features and fixes are part of this pull request:

- feat: allow freeze of model weights in training
- docs: fix typo in documentation
- ci: adjust workflow trigger
- fix: change latest macos workflow image for test pipeline


## 👀 Affected Areas

- Documentation
- Training
- Github Workflow (Test pipeline)

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [x] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

---------

Co-authored-by: github-actions &lt;action@github.com&gt;
Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt;
Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt; ([`1fee972`](https://github.com/codecentric-oss/niceml/commit/1fee972cafb87af971cf851088db41e12a3fdcb8))

## v0.14.1 (2024-04-16)

### Fix

* fix: test pipeline pendulum dependency ([`299426a`](https://github.com/codecentric-oss/niceml/commit/299426a27cfaf4f46e79958f600cdc1a8ad05466))

* fix: update poetry in Github pipelines to 1.7.1 ([`2d0dd2e`](https://github.com/codecentric-oss/niceml/commit/2d0dd2e2f250fe7517c12b68f7d36802ddd73964))

* fix: load non-parq files with DFLoader load_df ([`b693710`](https://github.com/codecentric-oss/niceml/commit/b693710fdf03962a543579342ba95b359b634974))

* fix: add original model id to eval experiment info ([`494c101`](https://github.com/codecentric-oss/niceml/commit/494c101fcd5993971cdb1b39895494cf6de82293))

### Style

* style: typos and comment movement ([`300299d`](https://github.com/codecentric-oss/niceml/commit/300299db9ad791df75397d83358bffb4519e8654))

## v0.14.0 (2024-02-08)

### Feature

* feat: update altair to 5.2.0 (#113)

## 📥 Pull Request Description

The current version of Altair raised multiple deprecation errors.
Therefore, altair is updated with this PR.

## 👀 Affected Areas

Dashboard

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`fbb72d4`](https://github.com/codecentric-oss/niceml/commit/fbb72d4111d806bffb4acaebe1a6ca43d5c82c33))

### Fix

* fix: simplify ExperimentManager using exp_dict ([`9a54dc9`](https://github.com/codecentric-oss/niceml/commit/9a54dc9ed954ab1a1a80a6964c9b7462d29b4b39))

* fix: query experiments based on storage handler name not mutable id ([`1e94add`](https://github.com/codecentric-oss/niceml/commit/1e94addf39393e328a566b0190fdaf7aab4aa4ac))

### Unknown

* Release preparation v0.13.2 (#115)

## 📥 Pull Request Description

The following changes, features and fixes are part of this pull request:
- fix: simplify ExperimentManager using exp_dict (#114)
- fix: query experiments based on storage handler name not mutable id
(#114)
- feat: update altair to 5.2.0 (#113)

## 👀 Affected Areas

- Dashboard
- Dependencies

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`34c5704`](https://github.com/codecentric-oss/niceml/commit/34c570427831ba69cf2d961cb44e7cb6e9e0e8a0))

* Merge branch &#39;main&#39; into develop ([`e24dea9`](https://github.com/codecentric-oss/niceml/commit/e24dea996dc192797a252260143f10bcf87a5845))

## v0.13.0 (2024-01-16)

### Ci

* ci(release): Sets the Python version of the release workflow to 3.10 ([`8e15200`](https://github.com/codecentric-oss/niceml/commit/8e15200fdcd94c7435d77e90b2a25dcadf720ac6))

* ci(test): Add workflow trigger `pull_request_target` to execute the workflow even with fork pull requests (#108)

## 📥 Pull Request Description

The following changes and fixes are part of this pull request:
- ci(test): Set pipeline trigger to `pull_request_target` to execute the
pipeline even with fork pull requests
- docs: Remove python 3.8 from Getting Started
- refactor: Remove python from classifiers in `pyproject.toml`
- ci(test): Add workflow trigger `pull_request` back into project

## 👀 Affected Areas

- pytest workflow
- docs

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] All tests ran successfully
- [X] All merge conflicts are resolved
- [X] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

## 📌 Related Issues

- closes #107 ([`9ae27f9`](https://github.com/codecentric-oss/niceml/commit/9ae27f9932ee55894f4bbce8bd279df4d891835c))

* ci(test): Add workflow trigger `pull_request_target` to execute the workflow even with fork pull requests (#108)

## 📥 Pull Request Description

The following changes and fixes are part of this pull request:
- ci(test): Set pipeline trigger to `pull_request_target` to execute the
pipeline even with fork pull requests
- docs: Remove python 3.8 from Getting Started
- refactor: Remove python from classifiers in `pyproject.toml`
- ci(test): Add workflow trigger `pull_request` back into project

## 👀 Affected Areas

- pytest workflow
- docs

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] All tests ran successfully
- [X] All merge conflicts are resolved
- [X] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

## 📌 Related Issues

- closes #107 ([`6a89c5f`](https://github.com/codecentric-oss/niceml/commit/6a89c5f87363e80726a75b0da6845d192a639ed8))

### Feature

* feat: Update tensorflow (`&gt;=2.13,&lt;=2.15`) and dagster (`~1.6.0`). Remove support for python `3.8` (#106)

## 📥 Pull Request Description

- Updated Dagster to Version 1.5 in order to leverage bug fixes in
dagster webservice
- Fix keras import error in order to enable usage of tensorflow 2.15

## 👀 Affected Areas

- Dagster Pipelines &amp; Webservice
- Tensorflow ML Backend

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [ ] All tests ran successfully
- [X] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

If this pull request is related to an existing issue, please reference
it here.

## 🔗 Links

Please provide any relevant links (e.g. documentation, external
resources) that support your changes.

## 📷 Screenshots

If applicable, please include screenshots of the before and after
effects of your changes.

Thank you for your contribution! 🎉

---------

Co-authored-by: Timo Schadt &lt;timo.schadt@alcon.com&gt; ([`71d82cc`](https://github.com/codecentric-oss/niceml/commit/71d82cce48042271d49eecf54813ffdbe53b4dc6))

* feat: Update tensorflow (`&gt;=2.13,&lt;=2.15`) and dagster (`~1.6.0`). Remove support for python `3.8` (#106)

## 📥 Pull Request Description

- Updated Dagster to Version 1.5 in order to leverage bug fixes in
dagster webservice
- Fix keras import error in order to enable usage of tensorflow 2.15

## 👀 Affected Areas

- Dagster Pipelines &amp; Webservice
- Tensorflow ML Backend

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [ ] All tests ran successfully
- [X] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

If this pull request is related to an existing issue, please reference
it here.

## 🔗 Links

Please provide any relevant links (e.g. documentation, external
resources) that support your changes.

## 📷 Screenshots

If applicable, please include screenshots of the before and after
effects of your changes.

Thank you for your contribution! 🎉

---------

Co-authored-by: Timo Schadt &lt;timo.schadt@alcon.com&gt; ([`9c3f6af`](https://github.com/codecentric-oss/niceml/commit/9c3f6af92059f890c9d5f8bebe4eae55966f16c2))

### Fix

* fix(ci): Set Python version to 3.11 due to an interpretation error of the Github actions ([`29bafbf`](https://github.com/codecentric-oss/niceml/commit/29bafbfb5c939292958a4428f7bf5d22e1382ae8))

* fix: changed tf-macos version to &lt;=2.14 ([`a84c6c4`](https://github.com/codecentric-oss/niceml/commit/a84c6c48d2626983f4ed934fa23d596c14c18127))

* fix: changed tf-macos version to &lt;=2.14 ([`5516531`](https://github.com/codecentric-oss/niceml/commit/55165313b6a5757f1e60d1dd39761bf4c6002d60))

## v0.12.0 (2024-01-04)

### Documentation

* docs: Adjust python version information in documentation ([`5ea5e93`](https://github.com/codecentric-oss/niceml/commit/5ea5e930244ff187a2acd73704908b19b1250475))

### Feature

* feat(Dependencies): Allow Python 3.11 and adapt dependency versions

Add python 3.11 to the test matrix in test workflow ([`a60a420`](https://github.com/codecentric-oss/niceml/commit/a60a420803e4a806c15e95d0a004a821aa0489a4))

### Fix

* fix(Dependencies): Set `tensorflow-io-gcs-filesystem` to `~0.33.0` ([`59a059f`](https://github.com/codecentric-oss/niceml/commit/59a059f9d2e27058779ca1630bdbdbe80bfc8f61))

## v0.11.0 (2023-12-20)

### Documentation

* docs(contribution): Add information about how conventional and non-conventional commits are handled in pull requests ([`ec12c19`](https://github.com/codecentric-oss/niceml/commit/ec12c19cef99d53396b2400622a8a853f5a73020))

* docs(DevEntSetup): Refactor hint for other than conda ([`bc5acfe`](https://github.com/codecentric-oss/niceml/commit/bc5acfe247eb2224224f24c30b07162fad17019b))

* docs(DevEnvSetup): Add hint for pipenv or other comparable solutions. Add recommendation for Apple Silicon ([`2c732f5`](https://github.com/codecentric-oss/niceml/commit/2c732f523874e4f7e800c33c685f1d8a0f3862b2))

* docs: Update contact information in `CODE_OF_CONDUCT` ([`9780565`](https://github.com/codecentric-oss/niceml/commit/978056505747f7beb1d459701cf20b8024d8a409))

* docs: add contribution guidelines and community standards into documentation ([`b209c4b`](https://github.com/codecentric-oss/niceml/commit/b209c4b24c6b732060960fca3abecb7f4e662984))

* docs: optimize coding standards ([`3810dcb`](https://github.com/codecentric-oss/niceml/commit/3810dcb24c1e9f612829e541369f96c17568db0d))

* docs: add `Commit Guidelines ` ([`c404b38`](https://github.com/codecentric-oss/niceml/commit/c404b383bf7df66cd841d9fae10a5d75300f36d0))

* docs: add `Developer Environment Setup Guide` ([`94d5e83`](https://github.com/codecentric-oss/niceml/commit/94d5e836f8076dfe3e1d048f8e393ddb8c5e1496))

* docs: Standardize headings ([`50805f7`](https://github.com/codecentric-oss/niceml/commit/50805f7b1251adbe5fea95ea34ac4cfa0676ec3b))

* docs: Add coding standards and contribution guidelines ([`3a64c22`](https://github.com/codecentric-oss/niceml/commit/3a64c22d67f4c072c9ac5e6ab27d26d4b156595f))

### Feature

* feat: add contribution guidelines to the project (#103)

## 📥 Pull Request Description

- docs: Add coding standards and contribution guidelines
- docs: Standardize headings
- docs: add `Developer Environment Setup Guide`
- docs: add `Commit Guidelines `
- docs: add contribution guidelines and community standards into
documentation
- docs: Update contact information in `CODE_OF_CONDUCT`
- docs(DevEnvSetup): Add hint for pipenv or other comparable solutions.
Add recommendation for Apple Silicon
- docs(DevEntSetup): Refactor hint for other than conda
- docs(contribution): Add information about how conventional and
non-conventional commits are handled in pull requests

## 👀 Affected Areas

- Repository core files like `CONTRIBUTION.md`
- docs

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] All tests ran successfully
- [X] All merge conflicts are resolved
- [X] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`b9ea55a`](https://github.com/codecentric-oss/niceml/commit/b9ea55af87908f6c75507aaf6930489fa3f2e20a))

* feat(MLflow): Allow logging of nested tuple or int metrics in the `TensorGraphAnalyzer`

Adjust and extend unit test cases for `metrics_dict_to_mlflow_metrics_dict` ([`daea28a`](https://github.com/codecentric-oss/niceml/commit/daea28a7d76e441d238a044b2973ccf57a27e35e))

* feat: change model custom objects and callbacks refactored ([`c6f9fd3`](https://github.com/codecentric-oss/niceml/commit/c6f9fd39d592559e8656eb07a1bff8d9816c16fa))

### Fix

* fix: rename tensorflow to keras ([`f38536f`](https://github.com/codecentric-oss/niceml/commit/f38536f802052ca50c60ec4c29d53923913a685c))

### Unknown

* release: preparation for different frameworks (#104)

## 📥 Pull Request Description

A part of this PR is the preparation for different ML frameworks
(pytorch or transformers).

## 👀 Affected Areas

The code was refactored and the configuration is changed.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`21b4cd0`](https://github.com/codecentric-oss/niceml/commit/21b4cd076eb3f7dc7c94ca2bb3029fbf006e5612))

* Merge branch &#39;develop&#39; into feature/add_contribution_docs ([`f21f474`](https://github.com/codecentric-oss/niceml/commit/f21f4745bfcbf6b3f2239b6b883ce064a1872a30))

* fix(`TensorGraphAnalyzer`):Insert metric key in exception message if float parsing or dict flattening fails ([`94feac2`](https://github.com/codecentric-oss/niceml/commit/94feac243cbfcb541350ff0d27c767cbecaabcbd))

* test (TensorGraphAnalyzer):  Add unit tests for `metrics_dict_to_mlflow_metrics_dict` ([`6327d87`](https://github.com/codecentric-oss/niceml/commit/6327d871378a1e40154c078e3725eb6a6e10cadf))

* fix (MLflow): Enable logging of nested metrics in the `TensorGraphAnalyzer` ([`04eac29`](https://github.com/codecentric-oss/niceml/commit/04eac29b89bfde91ac6c126b087af74410456463))

* Merge branch &#39;develop&#39; into feature/add_contribution_docs ([`7281232`](https://github.com/codecentric-oss/niceml/commit/72812322093e37013179d158b1e6dae16cdb894e))

* fix (Dataset): Make `DfDataset` and `GenericDataset` abstract (#101) ([`fb45374`](https://github.com/codecentric-oss/niceml/commit/fb453749e2f0ef630e6c1cdb9f39814326e0ff0d))

* feature: separate datasets to keras datasets for including other frameworks ([`2242721`](https://github.com/codecentric-oss/niceml/commit/2242721e0b48a8cb150f1a3eccdb1005b152ba4c))

* Merge branch &#39;main&#39; into develop ([`7af1125`](https://github.com/codecentric-oss/niceml/commit/7af112595dae3b7204b0d5a2634a66cc895b3d93))

## v0.10.0 (2023-12-12)

### Feature

* feat: optimize file locks (#94)

## 📥 Pull Request Description

Optimize FileLocks and add tests

## 👀 Affected Areas

All occurencies of the File locks and testing.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`907c169`](https://github.com/codecentric-oss/niceml/commit/907c169c257c30a158b32b9c15359bb1ed8100ec))

## v0.9.1 (2023-12-05)

### Fix

* fix: list_dir filter_ext (#93)

## 📥 Pull Request Description

The filter_ext filtering was performed before the files in the
subfolders were extracted (recursive logic). This led to Bug #91 .

## 👀 Affected Areas

Every list_dir, where the filter_ext is used.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

---------

Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt;
Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`d8171fb`](https://github.com/codecentric-oss/niceml/commit/d8171fb2dfd5c7620767e3b409263def521b8423))

### Unknown

* Merge branch &#39;main&#39; into develop ([`971b31e`](https://github.com/codecentric-oss/niceml/commit/971b31e83deaf535832d612481c290971bba96ae))

## v0.9.0 (2023-11-28)

### Feature

* feat: write and read json options in experiment context (#90)

## 📥 Pull Request Description

Added write and read options for json files to ExperimentContext.
This enables the user to write out additional Information, for example
target classes.

## 👀 Affected Areas

Trainings Pipelines

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`77d3dc9`](https://github.com/codecentric-oss/niceml/commit/77d3dc92b71087f3787ff6d51d5761f73e52c2a3))

* feat: write and read json options in experiment context (#90)

## 📥 Pull Request Description

Added write and read options for json files to ExperimentContext.
This enables the user to write out additional Information, for example
target classes.

## 👀 Affected Areas

Trainings Pipelines

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`1aa8bd5`](https://github.com/codecentric-oss/niceml/commit/1aa8bd537ed127ac299209e5d478bc5389650a91))

### Fix

* fix: pillow vulnerability and other + formatting (#89)

## 📥 Pull Request Description

Fix vulnerabilities and run some pre-commit hooks for reformatting
etc...

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed (not all green)
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

---------

Co-authored-by: Nils &lt;nils.uhrberg@codecentric.de&gt; ([`3d3e6af`](https://github.com/codecentric-oss/niceml/commit/3d3e6af88b2d353c136aec8ba7a825d899673087))

* fix: pillow vulnerability and other + formatting (#89)

## 📥 Pull Request Description

Fix vulnerabilities and run some pre-commit hooks for reformatting
etc...

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed (not all green)
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

---------

Co-authored-by: Nils &lt;nils.uhrberg@codecentric.de&gt; ([`9c62f3b`](https://github.com/codecentric-oss/niceml/commit/9c62f3b29b686b4d5c21bb46805a719b8a632c12))

### Unknown

* Merge branch &#39;main&#39; into develop ([`2161bdf`](https://github.com/codecentric-oss/niceml/commit/2161bdf17087a5c84f94e01f320967d393ee1eca))

## v0.8.3 (2023-11-08)

### Fix

* fix: Reload finished experiments in dashboard (#87)

## 📥 Pull Request Description

If the dashboard was started during a running experiment, the experiment
was visible in the dashboard but with incomplete information. Even after
the experiment was finished, the Cache was not updated, so the
experiment would still be incomplete in the dashboard.

This issue was fixed by checking for the latest modification in the
experiment files and updating the cache, if it was outdated.

Additionaly, the test pipeline was fixed, by defining the execution
sequence of tests.

## 👀 Affected Areas

- dashboard
- test pipeline

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

---------

Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt; ([`39764f5`](https://github.com/codecentric-oss/niceml/commit/39764f5238696881e1002e2a3b6e454457efe4c9))

* fix: Generate mkdocs graphs with multiple dependencies (#86)

## 📥 Pull Request Description

Implemented option to generate pipeline graphs of dagster jobs with
multiple op dependencies.

## 👀 Affected Areas

Documentation

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`ac56427`](https://github.com/codecentric-oss/niceml/commit/ac564270c8b1ea0cb3d8f7fa86ee0ceac639b4fc))

* fix: Replace lambda `class_extractor` in `DirClsDataInfoListing` with a private function because lambdas are not pickable (#85)

## 📥 Pull Request Description

Replace lambda `class_extractor` in `DirClsDataInfoListing` with a private function because lambdas are not pickable

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`def7d1a`](https://github.com/codecentric-oss/niceml/commit/def7d1ae08168ce2edef063268b9ae95b9c60f18))

* fix: Reload finished experiments in dashboard (#87)

## 📥 Pull Request Description

If the dashboard was started during a running experiment, the experiment
was visible in the dashboard but with incomplete information. Even after
the experiment was finished, the Cache was not updated, so the
experiment would still be incomplete in the dashboard.

This issue was fixed by checking for the latest modification in the
experiment files and updating the cache, if it was outdated.

Additionaly, the test pipeline was fixed, by defining the execution
sequence of tests.

## 👀 Affected Areas

- dashboard
- test pipeline

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

---------

Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt; ([`aafe59a`](https://github.com/codecentric-oss/niceml/commit/aafe59a160dd73d84697ddfa0ff26447139c32f5))

* fix: Generate mkdocs graphs with multiple dependencies (#86)

## 📥 Pull Request Description

Implemented option to generate pipeline graphs of dagster jobs with
multiple op dependencies.

## 👀 Affected Areas

Documentation

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`61488b2`](https://github.com/codecentric-oss/niceml/commit/61488b29cde38ecabda9c60188150724409ca757))

### Unknown

* Merge branch &#39;main&#39; into develop ([`de2bc1f`](https://github.com/codecentric-oss/niceml/commit/de2bc1fe3e4f6ea4925f3742c14d59bc347e3e0a))

## v0.8.2 (2023-10-09)

### Fix

* fix: add installation info to main documentation (#84)

## 📥 Pull Request Description

Added simple installation information to the main documentation page.

## 👀 Affected Areas

Documentation

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [x] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`10e60db`](https://github.com/codecentric-oss/niceml/commit/10e60dbc999e2e396a223d2bbc81f4329a807264))

* fix: add installation info to main documentation ([`b2f8c10`](https://github.com/codecentric-oss/niceml/commit/b2f8c10f1c0ab4a7e95ac08092f585f2f6a9ba46))

* fix: Replace lambda `class_extractor` in `DirClsDataInfoListing` with a private function because lambdas are not pickable (#85)

## 📥 Pull Request Description

Replace lambda `class_extractor` in `DirClsDataInfoListing` with a private function because lambdas are not pickable

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`98f25df`](https://github.com/codecentric-oss/niceml/commit/98f25df82a7275260f9588830cae727c2a21c0d5))

* fix: remove job flag to prevent multiple mlflow runs (#82)

## 📥 Pull Request Description

This pull request fixes a bug, which created two experiment runs out of
one dagster pipeline run. This is a bug, caused by the dagster
itegration of MLFlow. The implementation in niceML was correct. When the
bug of this package is fixed in the future, niceML may has to be updated
as well.
With this fix, niceML, dagster and MLFlow work and only one MLFlow
experiment run is created per dagster pipeline run.

## 👀 Affected Areas

Dagster Pipeline
MLFlow integration

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`31b3875`](https://github.com/codecentric-oss/niceml/commit/31b3875cf062d594afe42406fdb9dfeb6586c88e))

* fix: remove job flag to prevent multiple mlflow runs ([`8c8b78f`](https://github.com/codecentric-oss/niceml/commit/8c8b78f71dc514abe444b6f6bf125aaf707c38ea))

### Unknown

* Release preparation v0.8.2 (#83)

## 📥 Pull Request Description

This is the pull request for the merge into main before release v0.8.2
is published.
The following features, fixes and changes are part of this pull request
and the the release:

- fix: Create only one MLFlow run for one experiment (#82 )

## 👀 Affected Areas

- Dagster Pipeline
- MLFlow integration

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt; ([`1c04211`](https://github.com/codecentric-oss/niceml/commit/1c04211a678a87da7ee9a4afec2dd64fb689232a))

## v0.8.1 (2023-09-26)

### Fix

* fix: analysis now have credentials for datasets (#81)

## 📥 Pull Request Description

Fixed a bug that in the analysis step the credentials for the datasets
were not available.

## 👀 Affected Areas

pipelines, code

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

Thank you for your contribution! 🎉 ([`aeb6e63`](https://github.com/codecentric-oss/niceml/commit/aeb6e63846004a97c069d5849fb8fb34657d65d2))

### Unknown

* Merge branch &#39;main&#39; into fix/analysis_credentials_bug ([`9d26212`](https://github.com/codecentric-oss/niceml/commit/9d262122faa5e0b073e6ef88d96e93a9e83fae1e))

## v0.8.0 (2023-09-21)

### Ci

* ci: Copy config files to the template as part of the release workflow (#77)

## 📥 Pull Request Description

This pr fixes #75. As part of the release workflow, the project&#39;s
configuration files are copied to the template folder

## 👀 Affected Areas

- project template
- release workflow

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [x] Any necessary migrations have been run ([`de9605e`](https://github.com/codecentric-oss/niceml/commit/de9605ef44b7a19239e4a50760d036417240395b))

### Feature

* feat: Integrate mlflow in niceml (#79)

## 📥 Pull Request Description

Integrated mlflow in the train and eval job.

## 👀 Affected Areas

Affects code and tests.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [X] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [X] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

---------

Co-authored-by: Nils &lt;nils.uhrberg@codecentric.de&gt; ([`23aa7dc`](https://github.com/codecentric-oss/niceml/commit/23aa7dce5de354d00c674e61099522ee4cfda668))

* feat: Add predictionfunction and models as folder (#78)

## 📥 Pull Request Description

Allow models to be folders or files. Create a prediction function which
handles different prediction model types.

## 👀 Affected Areas

- documentation
- configuration
- implementation

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [ ] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`368c25c`](https://github.com/codecentric-oss/niceml/commit/368c25c18b3a2de3b82119fb74b7c3f3a4bd53ec))

### Fix

* fix: analysis now have credentials for datasets ([`87f7214`](https://github.com/codecentric-oss/niceml/commit/87f72148dbadab64370bb84004d8242127c1a558))

* fix: Return the experiment path instead of the `ExperimentInfo` if `exp_id` is not latest  (#76)

## 📥 Pull Request Description

There was a bug that the `get_exp_filepath` function returns
an`ExperimentInfo` instead of the experiment file path if the exp_id is
something else than &#34;latest&#34;. This is fixed with this pull request.

## 👀 Affected Areas

- eval pipeline --&gt; load experiment 

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`2d31041`](https://github.com/codecentric-oss/niceml/commit/2d310411d94aae32e8410b4b0299fc4b06620a4f))

### Unknown

* Release preparation v0.8.0 (#80) ([`a7f6bc1`](https://github.com/codecentric-oss/niceml/commit/a7f6bc152ef3265568e9bf62470519097daacf48))

* Merge branch &#39;main&#39; into develop ([`0832041`](https://github.com/codecentric-oss/niceml/commit/08320418356f7c7011cb135a8685fb53b5f3e609))

## v0.7.3 (2023-09-04)

### Unknown

* Release preparation v0.7.3 (#73)

## 📥 Pull Request Description

- fix: Optimize file locks and remove outdated template config (#72)
- fix: implemented image_size.from_pil image and size (#71)

## 👀 Affected Areas

- File Locks
- Image Size class

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

## 📌 Related Issues

None

## 🔗 Links

None

## 📷 Screenshots

None ([`f8ecb4a`](https://github.com/codecentric-oss/niceml/commit/f8ecb4a001d19088d9c40df24cdedaf054197850))

* Merge branch &#39;main&#39; into develop ([`77bba42`](https://github.com/codecentric-oss/niceml/commit/77bba42160f7b539d19b7c403fe12e7da9941644))

## v0.7.2 (2023-09-01)

### Fix

* fix: Remove Windows from documentation ([`0c252aa`](https://github.com/codecentric-oss/niceml/commit/0c252aa9e779f42233a810dd242d8934c3edeec9))

* fix: Remove `tensorflow-io-gcs-filesystem` as a dependency from the project template ([`ce4ea6c`](https://github.com/codecentric-oss/niceml/commit/ce4ea6c142cee8ecd611cc80a64863202bed3749))

* fix: Remove Windows as an option in `niceml init`. ([`a07cab4`](https://github.com/codecentric-oss/niceml/commit/a07cab4e641a1d9caf3b8f9b246382b397ed29d9))

* fix: Safely remove `tensorflow-io-gcs-filesystem` from `poetry-lock` ([`31515ca`](https://github.com/codecentric-oss/niceml/commit/31515cadd8c6c1eacaf2000cc6e7e135a4b73257))

* fix: Optimize file locks and remove outdated template config (#72)

## 📥 Pull Request Description

The &#39;is_acquired&#39; parameter of FileLocks can now be set when the Lock is
initialized. This can be necessary, if a FileLock file is already
present, but the according FileLock object is not. This may happen, if a
FileLock could not have been released e.g. due to an error.

Additionally, an outdated config was removed from a template
configuration.

## 👀 Affected Areas

Everywhere a FileLock is used.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run ([`dc374a6`](https://github.com/codecentric-oss/niceml/commit/dc374a639da2214cea77654e6da3a610f7a31aa5))

* fix: implemented image_size.from_pil image and size (#71)

## 📥 Pull Request Description

Now it is possible to create an ImageSize from an PIL image and also its
size.

## 👀 Affected Areas

tests, imagesize

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [x] Any necessary migrations have been run

Co-authored-by: Nils &lt;nils.uhrberg@codecentric.de&gt; ([`0643bf2`](https://github.com/codecentric-oss/niceml/commit/0643bf2c659d3d7d82c4bc9b6a9b46c8ba934e3c))

### Unknown

* Cleanup poetry lock (#70)

## 📥 Pull Request Description

Due to a possibly inconsistent `poetry.lock`, this has been cleaned up.
In addition, the following things have been implemented:

- fix: Remove Windows as an option in `niceml init`
- fix: Remove `tensorflow-io-gcs-filesystem` as a dependency from the
project template

## 👀 Affected Areas

- dependencies
- project template

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] All tests ran successfully
- [X] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

_None_ 

## 🔗 Links

_None_ 

## 📷 Screenshots

_None_ ([`da11b5e`](https://github.com/codecentric-oss/niceml/commit/da11b5e796dd004a4a30172126323dc17a5a4aa4))

* Merge branch &#39;main&#39; into develop ([`ed4f733`](https://github.com/codecentric-oss/niceml/commit/ed4f733415f7e2a7e049a52b1e2e05a2a9662093))

## v0.7.1 (2023-08-22)

### Fix

* fix: remove tensorflow-io-gcs-filesystem from dependencies (#69)

## 📥 Pull Request Description

Even though tensorflow-io-gcs-filesystem was declared as optional poetry
tried to install it when installing tensorflow-macos. That is why we
removed the unnecessary package.

## 👀 Affected Areas

Installation and dependencies.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [ ] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [ ] Any necessary migrations have been run

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`cfbadc8`](https://github.com/codecentric-oss/niceml/commit/cfbadc850e295a69f604a5431c98627fd66ae938))

### Unknown

* Merge branch &#39;main&#39; into develop ([`3bb24eb`](https://github.com/codecentric-oss/niceml/commit/3bb24ebb0538faa8a10fe0f4eca93fea5a75fbfc))

## v0.7.0 (2023-08-15)

### Unknown

* Release preparation  v0.7.0 (#67)

## 📥 Pull Request Description

The following changes and adjustment took place since the last release:

- fix: change type of  `image_path` in `load_img_uint8` (#55)
- docs: Add automatic generation of API documentation based on
docstrings (#54)
- fix: Update `cryptrography` to ^41.0.0
- fix: Update `requests` to ^2.13.0
- fix: Update `tornado` to ^6.3.2
- style(docu): add link how to add pycharm config for debugging
- style(docu): remove typos
- feat(Dependencies): Update of `dagster` to 1.4.x , `tensorflow`, and
the corresponding packages to 2.12.x (#60)
- feat: join location with path objects (#63)
- style: improved waittime messages for locks (#64)
- docs: add into to how to write a custom pipeline
- docs: add how to write a custom pipeline
- docs: add how to add a custom model
- docs: add how to start the pipeline via dagster-webserver
- feat: Improvements to `DfDataset` and other files to better perform
regression experiments (#56)


## 👀 Affected Areas

- docs
- dagster pipelines
- dependencies

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] All tests ran successfully
- [X] All merge conflicts are resolved
- [X] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

_None_

## 🔗 Links

_None_

## 📷 Screenshots

_None_ ([`e15d460`](https://github.com/codecentric-oss/niceml/commit/e15d46022cf9304e1b30cf5257756673932b716d))

* Merge branch &#39;main&#39; into develop ([`b9d28f5`](https://github.com/codecentric-oss/niceml/commit/b9d28f5efdce5c66bf7113c02a8f75f5faa83728))

## v0.6.1 (2023-08-02)

### Documentation

* docs: add PR feedback ([`84b6c6c`](https://github.com/codecentric-oss/niceml/commit/84b6c6ce2a11bc29a6431b8ebd8f16aa353bb332))

* docs: add how to start the pipeline via dagster-webserver ([`79a4db0`](https://github.com/codecentric-oss/niceml/commit/79a4db0014ce684fcec4d23ea923f02de52688ef))

* docs: add how to add a custom model ([`4027ef8`](https://github.com/codecentric-oss/niceml/commit/4027ef8727bbca24370aa703b26873618d4e627f))

* docs: add how to write a custom pipeline ([`66fe21c`](https://github.com/codecentric-oss/niceml/commit/66fe21c58fc60d5a355544ebb561a0e9612e9e59))

* docs: add into to how to write a custom pipeline ([`f0ec339`](https://github.com/codecentric-oss/niceml/commit/f0ec3395729a7362b0fc90754b4f000cbe37b50f))

* docs: Add automatic generation of API documentation based on docstrings (#54)

## 📥 Pull Request Description

API documentation is automatically generated based on the docstrings of
a package, module, class, function, and method. The navigation structure
is generated based on the package structure of niceML.

## 👀 Affected Areas

- docs 
- **DOCS NAVIGATION** - The navigation entries are now created via the
file `docs/SUMMARY.md`.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] All tests ran successfully
- [X] All merge conflicts are resolved
- [X] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

*None*

## 🔗 Links

*None*

## 📷 Screenshots

**Example API doc entry**

&lt;img width=&#34;1451&#34; alt=&#34;Bildschirmfoto 2023-07-20 um 15 48 32&#34;
src=&#34;https://github.com/codecentric-oss/niceml/assets/48205130/c4d76df3-38a2-4147-ad11-30bebcac7d1e&#34;&gt; ([`8a16e6f`](https://github.com/codecentric-oss/niceml/commit/8a16e6ffe9c80a446766721e078f869c256ed1fd))

### Feature

* feat: Improvements to `DfDataset` and other files to better perform regression experiments (#56)

## 📥 Pull Request Description

This pull request includes changes that specifically affect the
&#39;DfDataset&#39; or working with structured data. This includes the following
functions and corrections:

- feat: Load data (parquet) directly when initializing a `DfDataset`
- feat: Add some functions from the `GenericDataset` (`get_set_name`,
`get_batch_size`)
- fix: Add ZeroDevisionError into dataframe normalization
- fix: Optimize performance  of `get_datainfo`
- feat: Add `__getattr__` into `RegDataInfo`
- feat: Add denormalization for dataframe columns
- feat:  Add `FeatureTypes` for dataframe normalization
- feat: Add normalization functions and `NormalizationInfo`s for scalar,
categorical, and binary feature columns
- fix: Handling of columns with equal values during normalization
- feat: Add `FeatureCombiner` as part of the DfDataset
- fix: Remove deprecated `pandas.append` from `CSVLogger`
- fix: Remove superfluous `RemoteDiskDfLoader`
- feat: Use numbers tabular data for regression example

## 👀 Affected Areas

- `DfDataset`
- `DfLoader`
- Dataframe normalization
- Tests

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [ ] All tests ran successfully
- [X] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

_None_

## 🔗 Links

_None_

## 📷 Screenshots

_None_

---------

Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt; ([`f88abd8`](https://github.com/codecentric-oss/niceml/commit/f88abd8083a8202a4354f30e268b55a33037d9f4))

* feat: join location with path objects (#63)

## 📥 Pull Request Description

&#39;join_location_w_path&#39; now accepts a list of path objects, which will be
joined to the location. This way, one can now join a location with a
subfolder and its file in one step instead of having to call the
function multiple times.
The original functionality remains intact.

## 👀 Affected Areas

All areas where a location is joined with a path can now profit from the
change.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [x] Documentation has been updated to reflect the changes
- [x] Any necessary migrations have been run ([`d73286d`](https://github.com/codecentric-oss/niceml/commit/d73286d5980dda3048025a1f2508650b794de796))

* feat(Dependencies): Update of `dagster` to 1.4.x , `tensorflow`, and the corresponding packages to 2.12.x (#60)

## 📥 Pull Request Description

Due to various security vulnerabilities and version differences, it
makes sense to increase the `tensorflow` version. In this course, the
`dagster` version is also increased.

The following changes have been made:

- fix: removed decay from RMS prop config
- fix: Update requests to 2.31.0 (CVE-2023-32681)
- feat: Update of `dagster` to 1.4.x , `tensorflow`, and the
corresponding packages to 2.12.x


## 👀 Affected Areas

- Project dependencies

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] All tests ran successfully
- [X] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

Closes #62 

## 🔗 Links

_None_

## 📷 Screenshots

_None_

---------

Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt; ([`99b997e`](https://github.com/codecentric-oss/niceml/commit/99b997e460033ab97db86375b00deff8f5b77b29))

### Fix

* fix: Solve niceML installation issue due to pydantic and dagster version missmatsch(#57)

## 📥 Pull Request Description

The currently used version of `dagster` (`1.3.9`) does not work with the
latest version of `pydantic` (`2.x`). Due to this issue, it is necessary
to set the maximum allowed version of `pydantic` to `&lt;2.0` until dagster
fixes the problem.

Also, some security holes have been closed. 

## 👀 Affected Areas

- project dependencies
- 
## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] All tests ran successfully
- [X] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

_None_

## 🔗 Links

_None_

## 📷 Screenshots

_None_ ([`9303e19`](https://github.com/codecentric-oss/niceml/commit/9303e19f8f5080a93030f89a2b560dc081efc191))

* fix: Update `tornado` to ^6.3.2 ([`6315889`](https://github.com/codecentric-oss/niceml/commit/6315889213a422f6b27d75195d97e2d50017be69))

* fix: Update `requests` to ^2.13.0 ([`6559b64`](https://github.com/codecentric-oss/niceml/commit/6559b6466ea56bd204ad468c8fb65d0db8257e55))

* fix: Update `cryptrography` to ^41.0.0 ([`b188f99`](https://github.com/codecentric-oss/niceml/commit/b188f9913ad94c3045957d4dc0928d26d3fdd225))

* fix: Update `dagster` to ~1.3.13 ([`c842df0`](https://github.com/codecentric-oss/niceml/commit/c842df0dd2a01084438108a14ab509439772ff8f))

* fix: Set `pydantic` version to `&lt;2.0` ([`6b63ef1`](https://github.com/codecentric-oss/niceml/commit/6b63ef1b2b57653822419d26a71c89569a65a2cc))

* fix: PR feedback ([`bd6d475`](https://github.com/codecentric-oss/niceml/commit/bd6d475514ca1fa0a8538283da9b2ec52590aa3a))

* fix: PR feedback ([`c76a6e6`](https://github.com/codecentric-oss/niceml/commit/c76a6e6292d6d21e616043fd91d392cdfa72e9bb))

* fix: how to guide one yaml was false indented ([`61c023c`](https://github.com/codecentric-oss/niceml/commit/61c023c123e5fe153613f2b5b6505d73e940c470))

* fix: change type of  `image_path` in `load_img_uint8` (#55)

## 📥 Pull Request Description

load_img_uint8 did not work if image_path is not str but LocationConfig
type.

## 👀 Affected Areas

imageloading.py

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [x] Documentation has been updated to reflect the changes
- [x] Any necessary migrations have been run ([`7df85ee`](https://github.com/codecentric-oss/niceml/commit/7df85ee5ba3980a8b90e267e5a0b6f56c3254ef5))

### Style

* style: improved waittime messages for locks (#64)

## 📥 Pull Request Description

Give wait time information while waiting on file lock release.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [x] Documentation has been updated to reflect the changes
- [x] Any necessary migrations have been run ([`a08e76b`](https://github.com/codecentric-oss/niceml/commit/a08e76b015ebe50bf378c8c1a34f84b3e6b141fd))

* style(docu): add link how to add pycharm config for debugging ([`bbbd60d`](https://github.com/codecentric-oss/niceml/commit/bbbd60dfbf8f5fb03e9a9bc23127a9b1321f237e))

* style(docu): remove typos ([`fa0a301`](https://github.com/codecentric-oss/niceml/commit/fa0a301625c657262ebb4eab40468263e334160a))

### Unknown

* Docs/how to guide add a custom model (#65)

## 📥 Pull Request Description

3 sections were added to the documentation describing
1. How to write a custom pipeline
2. How to define a tensorflow sequential model using the niceml model
factory and integrate the model into the configuration structure
3. Run jobs using dagster-weberver

## 👀 Affected Areas

Documentation

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [x] Documentation has been updated to reflect the changes
- [x] Any necessary migrations have been run

## 📌 Related Issues

If this pull request is related to an existing issue, please reference
it here.

## 🔗 Links

Please provide any relevant links (e.g. documentation, external
resources) that support your changes.

## 📷 Screenshots

If applicable, please include screenshots of the before and after
effects of your changes.

Thank you for your contribution! 🎉 ([`3c345d5`](https://github.com/codecentric-oss/niceml/commit/3c345d54e4f73d63fd9296be3411e494f997319d))

* Merge branch &#39;develop&#39; into docs/how-to-guide-add-a-custom-model ([`d64db12`](https://github.com/codecentric-oss/niceml/commit/d64db12351cd360fd84cf8449028a082f7ab9db3))

* Add feature request issue template (#58)

## 📥 Pull Request Description

In addition to a bug report template, we also need a feature request
template. This pull request adds such a template to the repository as an
issue form.

## 👀 Affected Areas

- Issue template

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [ ] All tests ran successfully
- [X] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

_None_

## 🔗 Links

_None_

## 📷 Screenshots

_None_ ([`2b1efd1`](https://github.com/codecentric-oss/niceml/commit/2b1efd1f21fc29f8f2fc95ad04ade132dd5d47a0))

* Fix/typos in docu (#59)

## 📥 Pull Request Description

Typos and a false set link (how to add a pycharm config for debugging)
in the documenation were corrected.

## 👀 Affected Areas

Documenation.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [x] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [x] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [x] All tests ran successfully
- [x] All merge conflicts are resolved
- [x] Documentation has been updated to reflect the changes
- [x] Any necessary migrations have been run

## 📌 Related Issues

If this pull request is related to an existing issue, please reference
it here.

## 🔗 Links

Please provide any relevant links (e.g. documentation, external
resources) that support your changes.

## 📷 Screenshots

If applicable, please include screenshots of the before and after
effects of your changes.

Thank you for your contribution! 🎉 ([`73c25c5`](https://github.com/codecentric-oss/niceml/commit/73c25c51a069a4525c0090b06524ff82274fdd8f))

* Merge branch &#39;main&#39; into develop ([`7ee30b2`](https://github.com/codecentric-oss/niceml/commit/7ee30b2c819836276e93b860970af7c022ce5f7b))

## v0.6.0 (2023-07-10)

### Feature

* feat: Add `NanDataframeFilter` to drop nan values of feature columns (#51)

## 📥 Pull Request Description

A `DataframeFilter` is used to filter tabular data in a `DfDataset`. 
Besides the abstract implementation, a `NaNDataframeFilter` has also
been implemented, which removes rows with NaN values in the input and
target columns of the data description.

## 👀 Affected Areas

- `DataframeFilter` (**new**)

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [ ] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] All tests ran successfully
- [X] All merge conflicts are resolved
- [ ] Documentation has been updated to reflect the changes
- [x] Any necessary migrations have been run

## 📌 Related Issues

*None*

## 🔗 Links

_None_

## 📷 Screenshots

_None_ ([`3561200`](https://github.com/codecentric-oss/niceml/commit/3561200187c4073e2aec4631dd54572bd0686a11))

* feat: Add dagster op for dataframe normalization (#48)

## 📥 Pull Request Description

An option has been added to allow the normalization of data frames in a
`dagster` pipeline.
A list of features to be normalized can be specified. Alternatively, a
function can be passed that returns the feature columns.

## 👀 Affected Areas

- `dagster` pipelines

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [ ] Documentation has been updated to reflect the changes - **Not
necessary**
- [X] Any necessary migrations have been run

## 📌 Related Issues

*None*

## 🔗 Links

*None*

## 📷 Screenshots

*None* ([`fe0e8e0`](https://github.com/codecentric-oss/niceml/commit/fe0e8e07a3792ae830bddd5cdf904017f67d148b))

* feat: Add lockfile name as attribute of `FileChecksumProcessor ` (#46)

## 📥 Pull Request Description

To be more flexible in the configuration of a `FileChecksumProcessor` a
lock file name can now be specified. The default value is `lock.yaml`.

## 👀 Affected Areas

- `FileChecksumProcessor` and its subclasses

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [x] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [ ] Documentation has been updated to reflect the changes - **Not
necessary**
- [ ] Any necessary migrations have been run - **Not necessary**

## 📌 Related Issues

*None*

## 🔗 Links

*None*
## 📷 Screenshots

*None* ([`013addf`](https://github.com/codecentric-oss/niceml/commit/013addfdcf3d23de3c025a1e4c95b7c11fd0a0ac))

### Fix

* fix: Adjust supported python versions in `Getting Started` docs section ([`4bde794`](https://github.com/codecentric-oss/niceml/commit/4bde794d881d9c1c397d86a61bb040e1f96cbec8))

* fix: save result files from `tensorgraphanalyzer` at the correct place and implemented validation for that (#50)

Implemented a fix in the tensorgraphanalyzer to save the result files at
the correct location.
Improved the ExperimentSchemas to recognize such missing or incorrect
saved files. ([`ea3191b`](https://github.com/codecentric-oss/niceml/commit/ea3191b3c0fc31d7e435b30a74c16751c939a3b3))

* fix: Remove temp directory from hydra search path. Add hydra config mapping factory (#47)

## 📥 Pull Request Description

Until now, a temporary directory was always added to the search path of
a `dagster` configuration. This caused `dagster` to give an error
message when the configurations had to be searched.
The temporary directory is necessary for the operation with `dagit`,
because no configuration file has to be specified there, but directly
YAML code. In this pull request the temporary directory was removed from
the searchpath configuration.
Also, there is now a `hydra_conf_mapping_factory` that is used as a
decorator of a Dagster job, as this allows parameters to be passed and
overridden.

## 👀 Affected Areas

- Pipelines 

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [ ] Documentation has been updated to reflect the changes - **Not
necessary**
- [X] Any necessary migrations have been run 
- Pipelines run via a `dagster` script, but can also be started via
`dagit`.

## 📌 Related Issues

- closes #42 

## 🔗 Links

*None*

## 📷 Screenshots

`dagster` pipeline run

&lt;img width=&#34;1586&#34; alt=&#34;Bildschirmfoto 2023-07-05 um 08 08 35&#34;
src=&#34;https://github.com/codecentric-oss/niceml/assets/48205130/661a1cf7-7c01-45ed-bbdf-5f87abd9df26&#34;&gt;


`dagit` pipeline run 


![Capture-2023-07-05-080913](https://github.com/codecentric-oss/niceml/assets/48205130/785da3f9-eaf5-45eb-9bfb-8666317675dd) ([`6660ec9`](https://github.com/codecentric-oss/niceml/commit/6660ec91484c40fb21fdb3335e1244f24d757923))

### Unknown

* Release preparation  v0.6.0 (#52)

## 📥 Pull Request Description

The following features and fixes will be part of the next release
(`v0.6.0`)

- feat: Add lockfile name as attribute of `FileChecksumProcessor ` (#46)
- fix: Remove temp directory from hydra search path. Add hydra config
mapping factory (#47)
- fix: save result files from `tensorgraphanalyzer` at the correct place
and implemented validation for that (#50)
- feat: Add dagster op for dataframe normalization (#48)
- feat: Add `NanDataframeFilter` to drop nan values of feature columns
(#51)
- fix: Adjust supported python versions in `Getting Started` docs
section

Additionally, there are several adjustments to the project organization

- Pull request template added
- Bug Report template added
- Code of Conduct added

## 👀 Affected Areas

- `FileChecksumProcessor `
- dagster ops
   - `df_normalization`
- `DataframeFilter`
   - `NanDataframeFilter`
- `tensorgraphanalyzer` 
- docs

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] All tests ran successfully
- [X] All merge conflicts are resolved
- [X] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

_None_

## 🔗 Links

_None_

## 📷 Screenshots

_None_ ([`42e0f86`](https://github.com/codecentric-oss/niceml/commit/42e0f860f1800b51a7da1cacf8b65c55d2b74af7))

* Add `test` prefix to the name of  the test module of `nandataframefilter` ([`85bb16d`](https://github.com/codecentric-oss/niceml/commit/85bb16d1d77649ba4bcd29e02c7bc2eea4966b7e))

* Add Code of Conduct and Bug Report template ([`9b2e87a`](https://github.com/codecentric-oss/niceml/commit/9b2e87a8f7c58dab8202cd76c10b3ac0657d0e3e))

* Add pull request template ([`645140d`](https://github.com/codecentric-oss/niceml/commit/645140dd40c153134f7a3b3355820790eda68db6))

* Merge branch &#39;main&#39; into develop ([`25f32a2`](https://github.com/codecentric-oss/niceml/commit/25f32a226fc738fbb67da27828a7530c3ed83f47))

## v0.5.0 (2023-06-23)

### Feature

* feat: Add abstract `FileChecksumProcessor` and concrete class `ZippedCsvToParquetProcessor` (#44)

## 📥 Pull Request Description

With a FileChecksumProcessors, files from an input directory can be
processed and the results can then be saved in an output directory. The
checksums of input and output files are created and saved so that only
files that have changed are processed when executed again.

## 👀 Affected Areas

Core implementation. Mostly part of a sort of data preprocessing
pipeline.

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [ ] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues

*None*

## 🔗 Links

*None*

## 📷 Screenshots

*None*

---------

Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt; ([`a21d673`](https://github.com/codecentric-oss/niceml/commit/a21d67300705f3f1f4fc1515c567adef74ecfec5))

* feat: implementation of filelocks (#43)

Implemented read and writelocks for training and evaluation jobs. ([`9d4dacd`](https://github.com/codecentric-oss/niceml/commit/9d4dacd7e9b09a764f45fdf2dc1c5c701dc19535))

### Unknown

* Merge for new release - add file locks and `FileChecksumProcessors` (#45)

## 📥 Pull Request Description

A file lock implementation has been added, which can be used to lock
files/directories read or write. Furthermore, there are now
`FileChecksumProcessors`, which process data from an input directory and
store the results in an output directory. Thereby the checksums of the
files are formed

## 👀 Affected Areas

- dagster ops / jobs

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [X] Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)
- [X] Documentation has been updated to reflect the changes
- [X] Any necessary migrations have been run

## 📌 Related Issues
*None*

## 🔗 Links

*None*

## 📷 Screenshots

*None* ([`eaf2ee4`](https://github.com/codecentric-oss/niceml/commit/eaf2ee424f7d26bf5674b71f0bc77fdde37f0916))

* Merge branch &#39;main&#39; into develop ([`7d49056`](https://github.com/codecentric-oss/niceml/commit/7d49056eb179d8711e5881249b06bde50fa157e0))

* Adjust project template to current feature set (#40)

## 📥 Pull Request Description

The configurations (`yaml` files), part of the project template, are
incorrect or incomplete. In addition, the TensorFlow version stored in
the project template is still wrong (`2.8`).

With this pull request the configurations of the template were adjusted
and the TensorFlow version was changed to `2.9`.

## 👀 Affected Areas

- Project template (`./template`) 

## 📝 Checklist

Please make sure you&#39;ve completed the following tasks before submitting
this pull request:

- [X] Pre-commit hooks were executed
- [ ] Changes have been reviewed by at least one other developer
- [ ] ~~Tests have been added or updated to cover the changes (only
necessary if the changes affect the executable code)~~(**Not
necessary**)
- [ ] ~~Documentation has been updated to reflect the changes~~ (**Not
necessary**)
- [X] Any necessary migrations have been run

## 📌 Related Issues

Closes #35 , closes #36 

## 🔗 Links

Please provide any relevant links (e.g. documentation, external
resources) that support your changes.

## 📷 Screenshots

If applicable, please include screenshots of the before and after
effects of your changes. ([`a36a653`](https://github.com/codecentric-oss/niceml/commit/a36a653d36c47d40ae73e7c0cc3c2792d7188c54))

* Merge branch &#39;main&#39; into develop ([`fd3bf81`](https://github.com/codecentric-oss/niceml/commit/fd3bf81420844076a0f4d477a484f99cee9937fe))

## v0.4.1 (2023-06-22)

### Fix

* fix: Update the version of dagster to 1.3.9 (#34)

To close a vulnerability in `sqlalchemy` the version of `dagster` was
updated to `1.3.9`.
Fix #33 ([`118643d`](https://github.com/codecentric-oss/niceml/commit/118643d5742d189ba414d34080897390939cfd24))

* fix: added protobuf version (#32)

Added protobuf version for tf-macos

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`1ce7e8f`](https://github.com/codecentric-oss/niceml/commit/1ce7e8f2c25d7ba9035ad13ab7df6753e9746497))

### Unknown

* Merge branch &#39;main&#39; into develop ([`96f781d`](https://github.com/codecentric-oss/niceml/commit/96f781de6bc4d51fdc8c3cddbb90e63eb2ae836b))

## v0.4.0 (2023-06-05)

### Feature

* feat: Softmax for Semantic Segmentation (#30)

Add option to use a softmax for Semantic Segmentation
- implement void/background class
- adjust SemSegFocalLoss to correct alpha with void/background class ([`ec669b1`](https://github.com/codecentric-oss/niceml/commit/ec669b1bd9cf1c8e355707fcec75d3e1dcb50bde))

* feat: new tensorflow-metal version (#29)

added new tensorflow metal version ([`721842b`](https://github.com/codecentric-oss/niceml/commit/721842b2f656fe200634290015dad721aab05a61))

* feat: new tensorflow-metal version ([`e629895`](https://github.com/codecentric-oss/niceml/commit/e629895a8012edb7520c6d816e1dc961a46b621d))

### Unknown

* Update versions tf &amp; dagster, update softmax for semseg (#31)

- updated dagster
- updated tensorflow
- implemented Softmax for SemSeg
- added additional_dict option in hydraconfig for improved testing ([`ad1acd3`](https://github.com/codecentric-oss/niceml/commit/ad1acd3eac3e830b26f4de5becbec6f69d78faeb))

* Merge branch &#39;main&#39; into develop ([`2a2fa2b`](https://github.com/codecentric-oss/niceml/commit/2a2fa2b4fb514e97a55c724ff395026a6db3c65b))

* Remove links to subpages from index.md (#28)

To avoid dead links and be consistent with the documentation structure,
the `index.md` is adjusted.

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`9053a6f`](https://github.com/codecentric-oss/niceml/commit/9053a6ff81a1111e99968e93ae5e81d89cd99d62))

* Merge branch &#39;main&#39; into develop ([`aa5b2f3`](https://github.com/codecentric-oss/niceml/commit/aa5b2f386a2da3866ebf80e06474f0a5cea52104))

## v0.3.0 (2023-05-17)

### Feature

* feat: Add conversion of cropped_numbers_images to tabular data as an op ([`28bfafc`](https://github.com/codecentric-oss/niceml/commit/28bfafc58d53ac766a318056a751ab1b461d79fd))

* feat: Add albumentation for numbers dataset  image augmentation ([`8da7b24`](https://github.com/codecentric-oss/niceml/commit/8da7b248bc6691c05da54758aae4974f39ff9fe8))

### Fix

* fix: Adjust explanatory comments for albumentation ([`6f35f88`](https://github.com/codecentric-oss/niceml/commit/6f35f882645ca1e11d0815dba9fd1b5b13a0c94d))

* fix: Allow `None` as initial value for generating number images ([`55272e5`](https://github.com/codecentric-oss/niceml/commit/55272e55ec26cafddbed69172188c0a0779bda56))

* fix: Adjust the tests for image generation for albumentation ([`6db814c`](https://github.com/codecentric-oss/niceml/commit/6db814cf157657cbddee172b78d966dfd64d1345))

* fix: improvements that for eacht subset a row is written ([`5982ae3`](https://github.com/codecentric-oss/niceml/commit/5982ae3a715410ea1b354bd3891aefd7840c309f))

* fix: Replace weak md5 hash (CWE-327) ([`a438cc9`](https://github.com/codecentric-oss/niceml/commit/a438cc932830e39f04666486c2276d5cca57c679))

* fix: make all template env variables work by default ([`e7b7019`](https://github.com/codecentric-oss/niceml/commit/e7b70193aed4d5d5b6bd23dfc82e3155fbb0f955))

* fix: make all env variables work by default ([`9b25b78`](https://github.com/codecentric-oss/niceml/commit/9b25b78d69546f18a09e011b2a5fd3b56c4226c9))

* fix: transfer default for experiment_uri to files ([`1986cd6`](https://github.com/codecentric-oss/niceml/commit/1986cd64586cee07d6ab757175a304230dcab2cf))

* fix: Update `dagster` and add `dagit` (1.3.3) ([`66e4c9f`](https://github.com/codecentric-oss/niceml/commit/66e4c9f678a0b0f7adc3267c8cecff9b3596ab32))

* fix: Replace environment variable `OUTPUT_PATH` by `EXPERIMENT_URI` ([`d98858c`](https://github.com/codecentric-oss/niceml/commit/d98858c0fbd82fa66761a88aa06f58f730cb5e55))

* fix: Add default arguments to cli commands where reasonable ([`1727959`](https://github.com/codecentric-oss/niceml/commit/17279597b2888b3aea85d0983c7b26712c404393))

### Unknown

* Merge for release v0.3.0 (#25)

**Features**
- Convert images of the number dataset to tabular data as a new part of
the number dataset
- Add albumentation (for image augmentation) into the image generation
of the numbers dataset
- Expand documentation ([`255393f`](https://github.com/codecentric-oss/niceml/commit/255393ff1dc7befd46306a743d73c4f0479a6893))

* Use niceml cli in documentation (#23)

- rewrite &#39;Getting started&#39; tutorial in documentation to use &#39;niceml&#39;
cli
- add &#39;Generate test data&#39; section to documentation
- add &#39;Use the niceML Dashboard&#39; section to documentation
- fix download component in dashboard ([`9a88de0`](https://github.com/codecentric-oss/niceml/commit/9a88de092e2e039f07f7b8f664b3d3602e546b51))

* Merge branch &#39;develop&#39; into feature/use_niceml_package_in_docs

# Conflicts:
#	README.md
#	poetry.lock ([`75c070d`](https://github.com/codecentric-oss/niceml/commit/75c070d340014769da065fcf82ea3fe448abb30d))

* Add image augmentation to the background images of the numbers dataset (#22)

**Changes**

- use albumentation for image augemntation
- remove solid color backgrounds from the dataset


**Examples** 

![0a0d2b92](https://github.com/codecentric-oss/niceml/assets/48205130/07d15250-b035-4b91-93cd-a440dea1ae1d)

![0c419617](https://github.com/codecentric-oss/niceml/assets/48205130/5f7228c6-3030-45bf-8db5-2978af9e13fb) ([`a92c873`](https://github.com/codecentric-oss/niceml/commit/a92c8734c705b22e52a4bb4637cdfe2ee9db5e3f))

* Merge branch &#39;develop&#39; into feature/numbers-bg-augmentation ([`0326c39`](https://github.com/codecentric-oss/niceml/commit/0326c39d0aaad12acb59d8d5757fbee5578febcf))

* Expand numbers dataset with tabular data (#21)

- Added new op that converts the cropped images of the numbers dataset
into tabular values
- Add function to convert an image into a dataframe and also add tests 
- The dataframe (tabular data) has the following form

| identifier | label | px_0_0 | px_0_1 | ... |
| --- | --- | ---  | --- | --- |

- First detailed ruff  configuration 
   - Configure pylint and pydoc

&gt; Note
&gt; To disable a pylint rule, the comment `# noqa: &lt;Rule_ID&gt;` can be used

- Remove md5 hash due to
[CWE-327](https://cwe.mitre.org/data/definitions/327.html) ([`1cbd15d`](https://github.com/codecentric-oss/niceml/commit/1cbd15ddce00a43dfed92084c92b98b19e136cf0))

* add badges to readme

minor documentation changes
move mkdocs-table-reader-plugin to dev dependencies ([`13e5667`](https://github.com/codecentric-oss/niceml/commit/13e56676de5c146a6bde6f5c1b738d7aaaf840ae))

* add documentation for generating test data ([`6bd8560`](https://github.com/codecentric-oss/niceml/commit/6bd8560d128aaf757a2f7c2284aa9ab9f1e8b2d2))

* replace download component with zip-download

original download component was not working ([`3bfe56a`](https://github.com/codecentric-oss/niceml/commit/3bfe56a0d71201971af070b707271a332279a4c0))

* fix formatting bugs in niceml tutorial ([`3ec3359`](https://github.com/codecentric-oss/niceml/commit/3ec33592509fec95d04aef3ab1d215146bed728c))

* update niceml tutorial ([`440d3ee`](https://github.com/codecentric-oss/niceml/commit/440d3eeab3586c1963d281922071899d915018d2))

* update niceml tutorial ([`19a1027`](https://github.com/codecentric-oss/niceml/commit/19a1027ceff91d20974905e03260a2cc2d699189))

* Feature/add dagit (#20)

- update dagster to 1.3.3
- add dagit
- add defaults to cli commands
- replace &#39;OUTPUT&#39; env-variable with &#39;EXPERIMENT_URI&#39;

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt;
Co-authored-by: Anke Koke &lt;anke.koke@codecentric.de&gt; ([`b547587`](https://github.com/codecentric-oss/niceml/commit/b547587e04da52985d540ddf2e3ecd53abba82c4))

* Merge branch &#39;main&#39; into develop ([`2c1d54a`](https://github.com/codecentric-oss/niceml/commit/2c1d54a3e46da8732c1efb0cf703a82f762d366d))

## v0.2.0 (2023-05-10)

### Feature

* feat: Add `niceml init` as cli command to initialize a new niceml project  (#13)

- Add copier template
- Add copier script 
- Add cli command  `init`

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`4f3090a`](https://github.com/codecentric-oss/niceml/commit/4f3090acbc68db2d63f3d42ce7a20aa64f229643))

### Fix

* fix: resize bg_images in assets for smaller wheel size (#11)

- resize background images for data generation to smaller wheel size
- add conceptual documentation

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`da291f4`](https://github.com/codecentric-oss/niceml/commit/da291f4c230fa5a186f441432596e26eac4460fb))

### Unknown

* Set commit_version_number to true (#19)

- Set the concurrency of the build step to `build` (name of the job) so
that only one workflow instance can build a release at a time
- Semantic release configuration adjusted so that version changes are
transferred.

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`2aa02f8`](https://github.com/codecentric-oss/niceml/commit/2aa02f847eb956e9f15f7dad3a53b6a2d12e9df4))

* Merge branch &#39;main&#39; into develop ([`f37ce68`](https://github.com/codecentric-oss/niceml/commit/f37ce68d291038e401768e6f923e02ca82837db0))

* Fix project meta (#18)

- Use tool.poetry.urls to define a hompage

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`6fdef2c`](https://github.com/codecentric-oss/niceml/commit/6fdef2c462ecf52ecc0c164ec122ab5cdad8de7d))

* Fix classifiers (#17)

- Remove Framework classifiers 
- Fix spelling

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`9f992bd`](https://github.com/codecentric-oss/niceml/commit/9f992bdfe36f7c86c382b8d1d8a2f1e6137a502f))

* Add mkdocs to dev dependencies (#16)

- Adjust docs workflow
- Remove test job from release workflow

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`7becb9b`](https://github.com/codecentric-oss/niceml/commit/7becb9b9c8cfa5aa577d4585952f26bb145cb5cb))

* Add current features into main (#15)

- Add `niceml init`
- Fix background images
- Add more documentation ([`61a66c9`](https://github.com/codecentric-oss/niceml/commit/61a66c980e72bee2e4062f54c02a0fafb735010f))

* Merge branch &#39;main&#39; into develop

# Conflicts:
#	.github/workflows/docs.yaml
#	.github/workflows/pytest.yaml
#	.github/workflows/release.yaml
#	.pre-commit-config.yaml
#	Makefile
#	README.md
#	niceml/__init__.py
#	poetry.lock
#	pyproject.toml ([`354cb94`](https://github.com/codecentric-oss/niceml/commit/354cb94fa571fa8f753469d2d3f2f2f54341dc6a))

* Connect github-pages to custom domain (#14)

- add sample.env
- add pypi badge to readme ([`c22fe25`](https://github.com/codecentric-oss/niceml/commit/c22fe2577499830f94ca228e866d89b303cf877a))

* Add poetry extra for tensorflow windows and fix release pipeline (#12)

- Adapt Makefle
- Add need (test) to release job
- Improved project description

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`f08ebac`](https://github.com/codecentric-oss/niceml/commit/f08ebac4987eeb48be7747ef049a98ce11c0d1a6))

* Fix ref attribute of action/checkout (#10)

`ref` is a subparameter of `with`

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt; ([`3fd3415`](https://github.com/codecentric-oss/niceml/commit/3fd3415cc824c58ffe6b20789e60a146856b8daf))

* Fix release pipeline (#9)

- Version source is now tag
- mkdocs dependencies are installed as a poetry extra
- Set the publish pipeline trigger to closed pull request in main

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt;
Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt;
Co-authored-by: github-actions &lt;action@github.com&gt; ([`186a0f1`](https://github.com/codecentric-oss/niceml/commit/186a0f1647b516801174b0b29faa35510d481728))

* Fix release workflow (#8)

- Add optional mkdocs dev dependencies
- Change pre-commit hooks (ruff)
- Add write permission to release workflow

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt;
Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt;
Co-authored-by: github-actions &lt;action@github.com&gt;
Co-authored-by: Anke Koke &lt;79906866+ankeko@users.noreply.github.com&gt;
Co-authored-by: Denis Stalz-John &lt;dj.de.john@googlemail.com&gt; ([`44bfdbc`](https://github.com/codecentric-oss/niceml/commit/44bfdbc2473cfe9099f261212e74f99cae31a5ec))

* Grant write permission to release workflow ([`44fa254`](https://github.com/codecentric-oss/niceml/commit/44fa254481a6ead671529d3a7c9b2f7c24e43c37))

* Add github workflows and first documentation (#7)

fix: macos tensorflow

other:
- add first documentation
- add pre-commit hooks
- add pipeline for tests, documentation and release
- update to dagster 1.3.2

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt;
Co-authored-by: Denis Stalz-John &lt;denis.stalz-john@codecentric.de&gt;
Co-authored-by: Nils &lt;48205130+nuhrberg@users.noreply.github.com&gt;
Co-authored-by: github-actions &lt;action@github.com&gt;
Co-authored-by: Denis Stalz-John &lt;dj.de.john@googlemail.com&gt; ([`32dc68e`](https://github.com/codecentric-oss/niceml/commit/32dc68ec86719e9b4c11281e30fd094d46a4ed80))

* Merge branch &#39;main&#39; into develop ([`d363775`](https://github.com/codecentric-oss/niceml/commit/d3637757fec3359b4c13e8663de43b5f39f0cb14))

* Create CNAME ([`879f331`](https://github.com/codecentric-oss/niceml/commit/879f3310abec2534539448cf916e64a2b0b5a053))

* Move documentation build to release pipeline (#6) ([`5bb1fa6`](https://github.com/codecentric-oss/niceml/commit/5bb1fa67760a956243815b0ec049d71100bec90c))

* Update README.md

remove duplicated lined ([`fc90107`](https://github.com/codecentric-oss/niceml/commit/fc90107f8e9267e35661669b281c458e72b89336))

* Add first documentation (#5)

- add documentation page generated with MKDocs
- rename ccml to niceML
- add pre-commit hooks

---------

Co-authored-by: Denis Stalz-John &lt;dj.de.john@googlemail.com&gt; ([`2e6c016`](https://github.com/codecentric-oss/niceml/commit/2e6c016b854ec1f23e3e964e5488f72e66957845))

* Add GitHub actions for pytest and release (#4)

- A workflow is started, which runs the pytests in the repository, as
soon as a pull request is opened, reopened or changes are made.
- Tests are performed as a matrix configuration (os=[ubuntu-latest,
macos-latest], python=[&#34;3.8&#34;, &#34;3.9&#34;, &#34;3.10&#34;])
- A workflow is started when a pull request is merged into the main
branch. This first runs all pytests and then creates a new release.

---------

Co-authored-by: Nils Uhrberg &lt;nils.uhrberg@codecentric.de&gt;
Co-authored-by: github-actions &lt;action@github.com&gt; ([`e760446`](https://github.com/codecentric-oss/niceml/commit/e7604463edc417c86477a047c7197f7ea263d486))

* Update dagster version (#3)

Change versions to make all commands work again. ([`a18098e`](https://github.com/codecentric-oss/niceml/commit/a18098eeb037fd7f93531d9e8f84708c520f37d6))

* Merge remote-tracking branch &#39;origin/main&#39; into develop ([`b1bacf7`](https://github.com/codecentric-oss/niceml/commit/b1bacf7410655fc0101ef87460af5257e377b649))

## v0.1.1 (2023-04-28)

### Unknown

* Merge pull request #2 from codecentric-oss/feature/include_source

Feature/include source ([`1f945cd`](https://github.com/codecentric-oss/niceml/commit/1f945cd0b521a5704ba13f76324ae8d9102325c6))

* bump up version ([`24315eb`](https://github.com/codecentric-oss/niceml/commit/24315eb69893caa5c78ca21a5d18f77430dec17e))

* add experiments ([`071d954`](https://github.com/codecentric-oss/niceml/commit/071d954c3c763a4d1d7406c7837cf0e27c36a5b9))

* Merge pull request #1 from codecentric-oss/feature/include_source

Feature/include source ([`f35725a`](https://github.com/codecentric-oss/niceml/commit/f35725a2e1b95a9ff2848f3dbf19146879d19193))

* only one author ([`0a8b937`](https://github.com/codecentric-oss/niceml/commit/0a8b937d253e04fa307d6dbf95a321ed8e2f4ed7))

* First version of the source code ([`b7a1179`](https://github.com/codecentric-oss/niceml/commit/b7a11793a1ae1786466486772d871acc2e0a5287))

* commit pyproject and gitignore ([`da6cedb`](https://github.com/codecentric-oss/niceml/commit/da6cedb6c9d7ef24ba8bda9313156b994506a08e))

* Create LICENSE ([`023e829`](https://github.com/codecentric-oss/niceml/commit/023e8294d29ce8d5cc0ccdb2a4d2fd56c3aef54b))

* inital readme commit ([`196c7eb`](https://github.com/codecentric-oss/niceml/commit/196c7eb1cad1e14fab4ff11b72ad04d4c064f85f))
