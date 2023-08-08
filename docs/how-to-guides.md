# How-to Guides

This part of the project documentation focuses on a
**problem-oriented** approach. You'll tackle common
tasks that you might have, with the help of the code
provided in this project.

## How to debug my experiment

To debug your experiment, you need to add a run configuration to your
favorite IDE. Here is an example on [how to add a run configuration
in PyCharm](https://www.jetbrains.com/help/pycharm/creating-run-debug-configuration-for-tests.html).

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

## How to configure a custom pipeline
NiceML provides configurable, re-usable machine learning 
pipelines. NiceML comes with pre-configured pipelines for object detection, 
semantic semgmentation, regression, classification and others. But what if 
your problem is not covered (yet) by the pipeline portfolio niceML offers?
This guide will walk you through how to set up your first custom pipeline.
The goal of the pipeline is to orchestrate a classifier that can distinguish
between daisies and roses.

1. Download the images from [Kaggle](https://www.kaggle.com/datasets/alxmamaev/flowers-recognition)
and store the roses and daisies images in a `data` folder in your niceML project.
2. Let us start configuring at the highest level of niceML: The job 
configuration. For this, navigate to `configs/jobs/job_train/job_train_cls` 
and create a new file `job_train_cls_binary_flowers.yaml`.
3. Paste the content from `job_train_cls_binary.yaml` which is a good
starting point for our own pipeline.
4. Adjust job parameters in the configuration. Many parameters are 
pre-configured and do not require adjustment. However, we want to configure
our own **training**, **prediction**, **experiment_id** and
**input data location**. In the job configuration, we can already point
to the location where the Kaggle images are stored and to the dagster training and prediction
operation configurations we are going to write in the next step.
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
     - /ops/analysis@ops.analysis.config: op_analysis_cls_binary_flowers.yaml
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

5. Configure training operation
   1. We navigate to `configs/ops/train` and create `op_train_cls_binary_flowers.yaml`.
   2. We can use the content of `op_train_cls_binary_flowers.yaml` as a starting point 
   and change the definition where the training data is stored, what the image size
   is and which classes we use as labels. For the time being, we will use the
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

   4. You might have noticed, that we do not give a plain directory definition to tell
   niceml where the training images are stored. Instead, we define the datasets within
   a configuration yaml in `configs/shared/datasets/dataset_kaggle_flowers.yaml`. For now,
   we will use as the same configuration as in `dataset_cls_test.yaml`
6. Configure prediction operation
   1. We create `configs/ops/prediction/op_prediction_cls_binary_flowers.yaml` and use
   `op_prediction_cls.yaml` as a template.
   2. Here, we only have to change the definition of the training, validation and test datasets with
   the yaml we wrote in the step before (`dataset_kaggle_flowers.yaml`). The prediction configuration should look like this:
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
7. Start the pipeline using 
```python
niceml train configs/jobs/job_train/job_train_cls/job_train_cls_binary_flowers.yaml
```

## How to add a custom model
In order to define a custom model in niceML we can make use of the niceML `ModelFactory` class
and its ``create_model` function which could be implemented like this:
```python
from typing import Any

import tensorflow as tf
from keras import layers, Sequential, regularizers
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import OutputVectorDataDescription
from niceml.mlcomponents.models.modelfactory import ModelFactory
from niceml.utilities.commonutils import check_instance


class FlowerCNN(ModelFactory):
    def __init__(self, regulation_value: float, activation_function: str, final_activation: str):
        self.final_activation = final_activation
        self.activation_function = activation_function
        self.regulation_value = regulation_value

    def create_model(self, data_description: DataDescription) -> Any:
        input_dd: InputImageDataDescription = check_instance(
            data_description, InputImageDataDescription
        )
        output_dd: OutputVectorDataDescription = check_instance(
            data_description, OutputVectorDataDescription
        )

        in_layer = tf.keras.layers.Input(input_dd.get_input_tensor_shape())

        model = Sequential([
            in_layer,

            layers.Conv2D(16, 3, padding='same', activation=self.activation_function),
            layers.MaxPooling2D(),

            layers.Conv2D(32, 3, padding='same', activation=self.activation_function),
            layers.MaxPooling2D(),

            layers.Conv2D(64, 3, padding='same', activation=self.activation_function),
            layers.MaxPooling2D(),

            layers.Dropout(0.2),

            layers.Flatten(),

            layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(self.regulation_value)),
            layers.Dense(output_dd.get_output_size(), name="outputs", activation=self.final_activation)
        ])
        model.summary()
        return model

```
In the next step, we will integrate this model in the training operation configuration.
Simply change the target of the model setting to `nicemlproject.dir.of.custom.FlowerCNN`.

## How to implement a new dashboard component

More documentation will be provided soon.

## How to use a remote system in the dashboard

More documentation will be provided soon.

## How to use MinIO with niceML

More documentation will be provided soon.

## How to add a new custom metric

More documentation will be provided soon.
