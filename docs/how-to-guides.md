# How-to Guides

This part of the project documentation focuses on a
**problem-oriented** approach. You'll tackle common
tasks that you might have, with the help of the code
provided in this project.

## How to debug my experiment

To debug your experiment, you need to add a run configuration to your
favorite IDE. Here is an example on [how to add a run configuration
in PyCharm](#how-can-i-add-a-run-configuration-to-pycharm).

Some parts of the training need an additional configuration, to make
them debuggable. E.g. Debugging metrics, the loss or net callbacks. To
debug them, you need to set the `RUN_EAGERLY` parameter of your .env
file to `True`

## How to use my own run configuration for a niceML pipeline

niceML runs its pipelines via [dagster](https://dagster.io/).
If you want to start the pipelines in the terminal, just use the
following code snippet, replace the path and run it in your terminal. 

``` ssh
dagster job execute -m niceml.dagster.jobs.repository -j job_train -c configs/jobs/<path to your job yaml>
```

## How to configure the test data generation to my needs

Everything about test data generation and its adjustable parameters can
be found in the [Generating a Test Dataset with niceML](
generate-data.md#step-3-customizing-data-generation-optional)

## How to implement a new dashboard component

More documentation will be provided soon.

## How to use a remote system in the dashboard

More documentation will be provided soon.

## How to use MinIO with niceML

More documentation will be provided soon.

## How to add a new custom metric

More documentation will be provided soon.
