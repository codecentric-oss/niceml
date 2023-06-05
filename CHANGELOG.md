# Changelog

<!--next-version-placeholder-->

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
