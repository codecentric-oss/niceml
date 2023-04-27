"""Module for dagster op to generate test images (object detection / classification)"""

import json

from hydra.utils import ConvertMode, instantiate

from niceml.config.hydra import HydraInitField
from niceml.utilities.imagegeneration import NumberDataGenerator
from niceml.utilities.splitutils import clear_folder
from dagster import OpExecutionContext, op


@op(config_schema={"data_generator": HydraInitField(NumberDataGenerator)})
def data_generation(
    context: OpExecutionContext,
):
    """Generates random test image dataset based on a given `data_generator`"""

    op_config = json.loads(json.dumps(context.op_config))
    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)
    data_generator: NumberDataGenerator = instantiated_op_config["data_generator"]

    clear_folder(data_generator.location)
    output_location = data_generator.generate_images()

    return output_location
