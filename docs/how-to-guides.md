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

## How to add a custom model
In order to define a custom model in niceML we can make use of the niceML `ModelFactory` class
and its create_model function. To create a new model, implement yours by inheriting from 
the `ModelFactory` and configuring the functions you need. Here is an example:
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

## How to start the pipeline via the dagster UI?
You start dagster via
```bash 
dagster dev -m nicemltutorial.dagster.jobs.repository
```

and paste the job configuration of your choice to the launchpad.

## How to implement a new dashboard component

More documentation will be provided soon.

## How to use a remote system in the dashboard

More documentation will be provided soon.

## How to use MinIO with niceML

More documentation will be provided soon.

## How to add a new custom metric

More documentation will be provided soon.
