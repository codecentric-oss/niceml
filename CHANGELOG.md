# Changelog

<!--next-version-placeholder-->

## v0.9.0 (2023-11-28)

### Feature

* Write and read json options in experiment context ([#90](https://github.com/codecentric-oss/niceml/issues/90)) ([`77d3dc9`](https://github.com/codecentric-oss/niceml/commit/77d3dc92b71087f3787ff6d51d5761f73e52c2a3))

### Fix

* Pillow vulnerability and other + formatting ([#89](https://github.com/codecentric-oss/niceml/issues/89)) ([`3d3e6af`](https://github.com/codecentric-oss/niceml/commit/3d3e6af88b2d353c136aec8ba7a825d899673087))

## v0.8.3 (2023-11-08)

### Fix

* Reload finished experiments in dashboard ([#87](https://github.com/codecentric-oss/niceml/issues/87)) ([`39764f5`](https://github.com/codecentric-oss/niceml/commit/39764f5238696881e1002e2a3b6e454457efe4c9))
* Generate mkdocs graphs with multiple dependencies ([#86](https://github.com/codecentric-oss/niceml/issues/86)) ([`ac56427`](https://github.com/codecentric-oss/niceml/commit/ac564270c8b1ea0cb3d8f7fa86ee0ceac639b4fc))
* Replace lambda `class_extractor` in `DirClsDataInfoListing` with a private function because lambdas are not pickable ([#85](https://github.com/codecentric-oss/niceml/issues/85)) ([`def7d1a`](https://github.com/codecentric-oss/niceml/commit/def7d1ae08168ce2edef063268b9ae95b9c60f18))

## v0.8.2 (2023-10-09)

### Fix

* Add installation info to main documentation ([#84](https://github.com/codecentric-oss/niceml/issues/84)) ([`10e60db`](https://github.com/codecentric-oss/niceml/commit/10e60dbc999e2e396a223d2bbc81f4329a807264))
* Add installation info to main documentation ([`b2f8c10`](https://github.com/codecentric-oss/niceml/commit/b2f8c10f1c0ab4a7e95ac08092f585f2f6a9ba46))

## v0.8.1 (2023-09-26)

### Fix

* Analysis now have credentials for datasets ([#81](https://github.com/codecentric-oss/niceml/issues/81)) ([`aeb6e63`](https://github.com/codecentric-oss/niceml/commit/aeb6e63846004a97c069d5849fb8fb34657d65d2))
* Analysis now have credentials for datasets ([`87f7214`](https://github.com/codecentric-oss/niceml/commit/87f72148dbadab64370bb84004d8242127c1a558))

## v0.8.0 (2023-09-21)

### Feature

* Integrate mlflow in niceml ([#79](https://github.com/codecentric-oss/niceml/issues/79)) ([`23aa7dc`](https://github.com/codecentric-oss/niceml/commit/23aa7dce5de354d00c674e61099522ee4cfda668))
* Add predictionfunction and models as folder ([#78](https://github.com/codecentric-oss/niceml/issues/78)) ([`368c25c`](https://github.com/codecentric-oss/niceml/commit/368c25c18b3a2de3b82119fb74b7c3f3a4bd53ec))

### Fix

* Return the experiment path instead of the `ExperimentInfo` if `exp_id` is not latest ([#76](https://github.com/codecentric-oss/niceml/issues/76)) ([`2d31041`](https://github.com/codecentric-oss/niceml/commit/2d310411d94aae32e8410b4b0299fc4b06620a4f))

## v0.7.3 (2023-09-04)

### Fix

* Optimize file locks and remove outdated template config ([#72](https://github.com/codecentric-oss/niceml/issues/72)) ([`dc374a6`](https://github.com/codecentric-oss/niceml/commit/dc374a639da2214cea77654e6da3a610f7a31aa5))
* Implemented image_size.from_pil image and size ([#71](https://github.com/codecentric-oss/niceml/issues/71)) ([`0643bf2`](https://github.com/codecentric-oss/niceml/commit/0643bf2c659d3d7d82c4bc9b6a9b46c8ba934e3c))

## v0.7.2 (2023-09-01)

### Fix

* Remove Windows from documentation ([`0c252aa`](https://github.com/codecentric-oss/niceml/commit/0c252aa9e779f42233a810dd242d8934c3edeec9))
* Remove `tensorflow-io-gcs-filesystem` as a dependency from the project template ([`ce4ea6c`](https://github.com/codecentric-oss/niceml/commit/ce4ea6c142cee8ecd611cc80a64863202bed3749))
* Remove Windows as an option in `niceml init`. ([`a07cab4`](https://github.com/codecentric-oss/niceml/commit/a07cab4e641a1d9caf3b8f9b246382b397ed29d9))
* Safely remove `tensorflow-io-gcs-filesystem` from `poetry-lock` ([`31515ca`](https://github.com/codecentric-oss/niceml/commit/31515cadd8c6c1eacaf2000cc6e7e135a4b73257))

## v0.7.1 (2023-08-22)

### Fix

* Remove tensorflow-io-gcs-filesystem from dependencies ([#69](https://github.com/codecentric-oss/niceml/issues/69)) ([`cfbadc8`](https://github.com/codecentric-oss/niceml/commit/cfbadc850e295a69f604a5431c98627fd66ae938))

## v0.7.0 (2023-08-15)

### Feature

* Improvements to `DfDataset` and other files to better perform regression experiments ([#56](https://github.com/codecentric-oss/niceml/issues/56)) ([`f88abd8`](https://github.com/codecentric-oss/niceml/commit/f88abd8083a8202a4354f30e268b55a33037d9f4))
* Join location with path objects ([#63](https://github.com/codecentric-oss/niceml/issues/63)) ([`d73286d`](https://github.com/codecentric-oss/niceml/commit/d73286d5980dda3048025a1f2508650b794de796))
* **Dependencies:** Update of `dagster` to 1.4.x , `tensorflow`, and the corresponding packages to 2.12.x ([#60](https://github.com/codecentric-oss/niceml/issues/60)) ([`99b997e`](https://github.com/codecentric-oss/niceml/commit/99b997e460033ab97db86375b00deff8f5b77b29))

### Fix

* PR feedback ([`bd6d475`](https://github.com/codecentric-oss/niceml/commit/bd6d475514ca1fa0a8538283da9b2ec52590aa3a))
* PR feedback ([`c76a6e6`](https://github.com/codecentric-oss/niceml/commit/c76a6e6292d6d21e616043fd91d392cdfa72e9bb))
* How to guide one yaml was false indented ([`61c023c`](https://github.com/codecentric-oss/niceml/commit/61c023c123e5fe153613f2b5b6505d73e940c470))
* Change type of  `image_path` in `load_img_uint8` ([#55](https://github.com/codecentric-oss/niceml/issues/55)) ([`7df85ee`](https://github.com/codecentric-oss/niceml/commit/7df85ee5ba3980a8b90e267e5a0b6f56c3254ef5))

### Documentation

* Add PR feedback ([`84b6c6c`](https://github.com/codecentric-oss/niceml/commit/84b6c6ce2a11bc29a6431b8ebd8f16aa353bb332))
* Add how to start the pipeline via dagster-webserver ([`79a4db0`](https://github.com/codecentric-oss/niceml/commit/79a4db0014ce684fcec4d23ea923f02de52688ef))
* Add how to add a custom model ([`4027ef8`](https://github.com/codecentric-oss/niceml/commit/4027ef8727bbca24370aa703b26873618d4e627f))
* Add how to write a custom pipeline ([`66fe21c`](https://github.com/codecentric-oss/niceml/commit/66fe21c58fc60d5a355544ebb561a0e9612e9e59))
* Add into to how to write a custom pipeline ([`f0ec339`](https://github.com/codecentric-oss/niceml/commit/f0ec3395729a7362b0fc90754b4f000cbe37b50f))
* Add automatic generation of API documentation based on docstrings ([#54](https://github.com/codecentric-oss/niceml/issues/54)) ([`8a16e6f`](https://github.com/codecentric-oss/niceml/commit/8a16e6ffe9c80a446766721e078f869c256ed1fd))

## v0.6.1 (2023-08-02)

### Fix

* Solve niceML installation issue due to pydantic and dagster version missmatsch(#57) ([`9303e19`](https://github.com/codecentric-oss/niceml/commit/9303e19f8f5080a93030f89a2b560dc081efc191))
* Update `tornado` to ^6.3.2 ([`6315889`](https://github.com/codecentric-oss/niceml/commit/6315889213a422f6b27d75195d97e2d50017be69))
* Update `requests` to ^2.13.0 ([`6559b64`](https://github.com/codecentric-oss/niceml/commit/6559b6466ea56bd204ad468c8fb65d0db8257e55))
* Update `cryptrography` to ^41.0.0 ([`b188f99`](https://github.com/codecentric-oss/niceml/commit/b188f9913ad94c3045957d4dc0928d26d3fdd225))
* Update `dagster` to ~1.3.13 ([`c842df0`](https://github.com/codecentric-oss/niceml/commit/c842df0dd2a01084438108a14ab509439772ff8f))
* Set `pydantic` version to `<2.0` ([`6b63ef1`](https://github.com/codecentric-oss/niceml/commit/6b63ef1b2b57653822419d26a71c89569a65a2cc))

## v0.6.0 (2023-07-10)
### Feature
* Add `NanDataframeFilter` to drop nan values of feature columns ([#51](https://github.com/codecentric-oss/niceml/issues/51)) ([`3561200`](https://github.com/codecentric-oss/niceml/commit/3561200187c4073e2aec4631dd54572bd0686a11))
* Add dagster op for dataframe normalization ([#48](https://github.com/codecentric-oss/niceml/issues/48)) ([`fe0e8e0`](https://github.com/codecentric-oss/niceml/commit/fe0e8e07a3792ae830bddd5cdf904017f67d148b))
* Add lockfile name as attribute of `FileChecksumProcessor ` ([#46](https://github.com/codecentric-oss/niceml/issues/46)) ([`013addf`](https://github.com/codecentric-oss/niceml/commit/013addfdcf3d23de3c025a1e4c95b7c11fd0a0ac))

### Fix
* Adjust supported python versions in `Getting Started` docs section ([`4bde794`](https://github.com/codecentric-oss/niceml/commit/4bde794d881d9c1c397d86a61bb040e1f96cbec8))
* Save result files from `tensorgraphanalyzer` at the correct place and implemented validation for that ([#50](https://github.com/codecentric-oss/niceml/issues/50)) ([`ea3191b`](https://github.com/codecentric-oss/niceml/commit/ea3191b3c0fc31d7e435b30a74c16751c939a3b3))
* Remove temp directory from hydra search path. Add hydra config mapping factory ([#47](https://github.com/codecentric-oss/niceml/issues/47)) ([`6660ec9`](https://github.com/codecentric-oss/niceml/commit/6660ec91484c40fb21fdb3335e1244f24d757923))

## v0.5.0 (2023-06-23)
### Feature
* Add abstract `FileChecksumProcessor` and concrete class `ZippedCsvToParquetProcessor` ([#44](https://github.com/codecentric-oss/niceml/issues/44)) ([`a21d673`](https://github.com/codecentric-oss/niceml/commit/a21d67300705f3f1f4fc1515c567adef74ecfec5))
* Implementation of filelocks ([#43](https://github.com/codecentric-oss/niceml/issues/43)) ([`9d4dacd`](https://github.com/codecentric-oss/niceml/commit/9d4dacd7e9b09a764f45fdf2dc1c5c701dc19535))

### Fix
* Added protobuf version ([#32](https://github.com/codecentric-oss/niceml/issues/32)) ([`1ce7e8f`](https://github.com/codecentric-oss/niceml/commit/1ce7e8f2c25d7ba9035ad13ab7df6753e9746497))

## v0.4.1 (2023-06-22)
### Fix
* Update the version of dagster to 1.3.9 ([#34](https://github.com/codecentric-oss/niceml/issues/34)) ([`118643d`](https://github.com/codecentric-oss/niceml/commit/118643d5742d189ba414d34080897390939cfd24))

## v0.4.0 (2023-06-05)
### Feature
* Softmax for Semantic Segmentation ([#30](https://github.com/codecentric-oss/niceml/issues/30)) ([`ec669b1`](https://github.com/codecentric-oss/niceml/commit/ec669b1bd9cf1c8e355707fcec75d3e1dcb50bde))
* New tensorflow-metal version ([#29](https://github.com/codecentric-oss/niceml/issues/29)) ([`721842b`](https://github.com/codecentric-oss/niceml/commit/721842b2f656fe200634290015dad721aab05a61))
* New tensorflow-metal version ([`e629895`](https://github.com/codecentric-oss/niceml/commit/e629895a8012edb7520c6d816e1dc961a46b621d))

## v0.3.0 (2023-05-17)
### Feature
* Add albumentation for numbers dataset  image augmentation ([`8da7b24`](https://github.com/codecentric-oss/niceml/commit/8da7b248bc6691c05da54758aae4974f39ff9fe8))
* Add conversion of cropped_numbers_images to tabular data as an op ([`28bfafc`](https://github.com/codecentric-oss/niceml/commit/28bfafc58d53ac766a318056a751ab1b461d79fd))

### Fix
* Adjust explanatory comments for albumentation ([`6f35f88`](https://github.com/codecentric-oss/niceml/commit/6f35f882645ca1e11d0815dba9fd1b5b13a0c94d))
* Allow `None` as initial value for generating number images ([`55272e5`](https://github.com/codecentric-oss/niceml/commit/55272e55ec26cafddbed69172188c0a0779bda56))
* Adjust the tests for image generation for albumentation ([`6db814c`](https://github.com/codecentric-oss/niceml/commit/6db814cf157657cbddee172b78d966dfd64d1345))
* Improvements that for eacht subset a row is written ([`5982ae3`](https://github.com/codecentric-oss/niceml/commit/5982ae3a715410ea1b354bd3891aefd7840c309f))
* Replace weak md5 hash (CWE-327) ([`a438cc9`](https://github.com/codecentric-oss/niceml/commit/a438cc932830e39f04666486c2276d5cca57c679))
* Make all template env variables work by default ([`e7b7019`](https://github.com/codecentric-oss/niceml/commit/e7b70193aed4d5d5b6bd23dfc82e3155fbb0f955))
* Make all env variables work by default ([`9b25b78`](https://github.com/codecentric-oss/niceml/commit/9b25b78d69546f18a09e011b2a5fd3b56c4226c9))
* Transfer default for experiment_uri to files ([`1986cd6`](https://github.com/codecentric-oss/niceml/commit/1986cd64586cee07d6ab757175a304230dcab2cf))
* Update `dagster` and add `dagit` (1.3.3) ([`66e4c9f`](https://github.com/codecentric-oss/niceml/commit/66e4c9f678a0b0f7adc3267c8cecff9b3596ab32))
* Replace environment variable `OUTPUT_PATH` by `EXPERIMENT_URI` ([`d98858c`](https://github.com/codecentric-oss/niceml/commit/d98858c0fbd82fa66761a88aa06f58f730cb5e55))
* Add default arguments to cli commands where reasonable ([`1727959`](https://github.com/codecentric-oss/niceml/commit/17279597b2888b3aea85d0983c7b26712c404393))

## v0.2.0 (2023-05-10)
### Feature
* Add `niceml init` as cli command to initialize a new niceml project ([#13](https://github.com/codecentric-oss/niceml/issues/13)) ([`4f3090a`](https://github.com/codecentric-oss/niceml/commit/4f3090acbc68db2d63f3d42ce7a20aa64f229643))

### Fix
* Resize bg_images in assets for smaller wheel size ([#11](https://github.com/codecentric-oss/niceml/issues/11)) ([`da291f4`](https://github.com/codecentric-oss/niceml/commit/da291f4c230fa5a186f441432596e26eac4460fb))
