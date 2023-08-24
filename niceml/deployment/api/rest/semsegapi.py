"""Module of the SemSeg REST API service"""

import click
import numpy as np
from PIL import Image

from niceml.dagster.ops.prediction import is_numpy_output
from niceml.data.datadescriptions.semsegdatadescritption import SemSegDataDescription
from niceml.deployment.api.rest.rest import RestApi
from niceml.utilities.commonutils import check_instance
from niceml.utilities.encoding import base64_to_bytesio, numpy_to_base64


class SemSegApi(RestApi):
    """Implementation of `RestApi` to serve a REST-API for SemSeg experiments"""

    def add_routes(self):
        """Implementation of the abstract `add_routes` function."""

    def _predict(self, input_data: dict) -> dict:
        """
        Implementation of the predict endpoint of the SemSeg REST API. The input_data dict
        contains an `image` that is base64 encoded. This image is reformatted into a numpy
        array and scaled according to the `data_description`. The result of the model is
        returned as a base64-encoded image in a dictionary with the `pred` key.

        Args:
            input_data: The input data to the _predict function. In this case a dict with the key
                        `image` and a base64 encoded image as a value
        Returns:
            A dictionary with a single key `pred` and the value of this key is a base64
            encoded image
        """
        input_image = Image.open(base64_to_bytesio(input_data["image"])).convert("RGB")
        data_description: SemSegDataDescription = check_instance(
            self.assets["data_description"], SemSegDataDescription
        )
        input_image = input_image.resize(data_description.get_input_image_size().to_pil_size())
        prediction = (
            self.assets["model"]
            .predict_step(np.array([np.asarray(input_image, dtype=np.uint8)]))
            .numpy()
        )
        if not is_numpy_output(prediction):
            prediction = prediction.detach().numpy()
        values = np.max(prediction[0], axis=2) * 255
        value_idxes = np.argmax(prediction[0], axis=2)
        target_array = np.stack((values, value_idxes, np.zeros_like(values)), axis=2).astype(
            dtype=np.uint8
        )
        return {"pred": numpy_to_base64(target_array)}


@click.command()
@click.argument("host")
@click.argument("port")
def run_cmd(
    host: str,
    port: int,
):
    """
    The run_cmd function is the entry point for the SemSegApi.
    It will start a server on `host`:`port` and listen for requests.

    Args:
        host: The host IP address of the server
        port: The port number that the api will run on
    """
    api = SemSegApi()
    api.run(host, int(port))


if __name__ == "__main__":
    run_cmd()
