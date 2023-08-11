# Writing a new training pipeline

This tutorial will walk you through how to set up your first custom training pipeline.
The goal of this example pipeline is to orchestrate a classifier that can distinguish
between daisies and roses.

In this tutorial we will 
- learn which configuration yaml files we have to write to get our pipeline running
- have a look how the dataset, training, prediction, etc. configurations are connected with each other 
- train a binary classifier with niceML

## Prerequisites
Before we get started, please ensure that you have followed the [Getting Started](getting-started.md)
tutorial and initialized a new niceML project.

## Step 1: Data ingestion
Download the images from [Kaggle](https://www.kaggle.com/datasets/alxmamaev/flowers-recognition)
and store the roses and daisies images in a `data` folder in your niceML project.

## Step 2: Configure the pipeline job
Let us start configuring at the highest level of niceML: The job 
configuration. For this, navigate to `configs/jobs/job_train/job_train_cls` 
and create a new file `job_train_cls_binary_flowers.yaml`.

Paste the content of `configs/jobs/job_train/job_train_cls/job_train_cls_binary.yaml` which is a good
starting point for our own pipeline.

Adjust job parameters in `job_train_cls_binary_flowers.yaml`. Many parameters 
are pre-configured and do not require adjustment. However, we want to configure
our own 
- **training** and **prediction** ops (`/ops/train@ops.train.config`, `/ops/train@ops.prediction.config`), 
- **experiment_id** (`globals` -> `exp_name` and `exp_prefix`)
- and **input data location** (`globals` -> `data_location`). 
 
In the job configuration, we can already point
to the location where the Kaggle images are stored. 
Also, we change the path to the 
dagster training and prediction operation configurations we are going to write in
the next two steps.

```yaml
# train binary classification
defaults:
  # experiment
  - ops/experiment@ops.experiment.config: op_experiment_default.yaml
  # train
  - /ops/train@ops.train.config: op_train_cls_binary_flowers.yaml
  # prediction
  - /ops/prediction@ops.prediction.config: op_prediction_cls_binary_flowers.yaml
  # analysis
  - /ops/analysis@ops.analysis.config: op_analysis_cls_binary.yaml
  # experiment tests
  - /ops/exptests@ops.exptests.config.tests: exptests_default.yaml
  # experiment locations
  - shared/locations@globals: exp_locations.yaml
  - _self_

hydra:
  searchpath:
    - file://configs

globals:
  exp_name: FlowersClsBinary
  exp_prefix: FLOWERSCLB
  data_location:
    uri: ${oc.env:DATA_URI,./data}/kaggle_flowers
```

## Step 3: Configure the training operation
We navigate to `configs/ops/train` and create `op_train_cls_binary_flowers.yaml`.

We can use the content of `op_train_cls_binary_flowers.yaml` as a starting point 
and change the definition where the training data is stored, what the image size
is and which classes we use as labels. 

This means, we have to edit
- `/shared/datasets@data_train`
- `/shared/datasets@data_validation`
- `classes`
- `target_size width` and `target_size height`

For the time being, we will use the
OwnMobileNetModel model of Tensorflow and do not implement our own model definition.

```yaml
defaults:
  - op_train_base.yaml@_here_
  - /shared/datasets@data_train: dataset_kaggle_flowers.yaml
  - /shared/datasets@data_validation: dataset_kaggle_flowers.yaml
  - _self_
train_params:
  epochs: 5
data_description:
  _target_: niceml.data.datadescriptions.clsdatadescription.ClsDataDescription
  classes:
  - "daisy"
  - "roses"
  use_binary: true
  target_size:
    _target_: niceml.utilities.imagesize.ImageSize
    width: 180
    height: 180

data_train:
  datainfo_listing:
    sub_dir: train
  set_name: train
  shuffle: true
data_validation:
  datainfo_listing:
    sub_dir: validation
  set_name: validation
model:
  _target_: niceml.dlframeworks.tensorflow.models.mobilenet.OwnMobileNetModel
  final_activation: sigmoid
model_load_custom_objects:
  _target_: niceml.mlcomponents.modelcompiler.modelcustomloadobjects.ModelCustomLoadObjects
learner:
  _target_: niceml.dlframeworks.tensorflow.learners.defaultlearner.DefaultLearner
  model_compiler:
    _target_: niceml.dlframeworks.tensorflow.modelcompiler.defaultmodelcompiler.DefaultModelCompiler
    loss: binary_crossentropy
    # Optimizer used in the experiment
    optimizer:
      _target_: tensorflow.keras.optimizers.Adam
      learning_rate: 0.0001
    metrics: [ "accuracy" ]   
```

You might have noticed, that we did not give a plain directory definition to tell
niceml where the training images are stored. Instead, we define the datasets within
a configuration yaml in `configs/shared/datasets/dataset_kaggle_flowers.yaml`. For now,
we will use as the same configuration as in `dataset_cls_test.yaml`

## Step 4: Configure the prediction operation
We create `configs/ops/prediction/op_prediction_cls_binary_flowers.yaml` and use
`op_prediction_cls.yaml` as a template.

Here, we only have to change the definition of the training, validation and test datasets with
the yaml we wrote in the step before (`dataset_kaggle_flowers.yaml`). 
The prediction configuration should look like this:
   
```yaml
      defaults:
   - /shared/datasets@datasets.validation: dataset_kaggle_flowers.yaml
   - /shared/datasets@datasets.test: dataset_kaggle_flowers.yaml
   - /shared/datasets@datasets.train_eval: dataset_kaggle_flowers.yaml
   - prediction_handler: prediction_handler_vector.yaml
   - datasets: datasets_generic_default.yaml
   - op_prediction_base.yaml@_here_
   - _self_
```

## (Optional) Step 5: Add a custom model
If you want to add a custom model have a look at the
[How to add a custom model](how-to-guides.md#How to add a custom model).

## Step 6: Start the pipeline
Run niceML and hand over the top-level jon configuration file via

```python
niceml train configs/jobs/job_train/job_train_cls/job_train_cls_binary_flowers.yaml
```
