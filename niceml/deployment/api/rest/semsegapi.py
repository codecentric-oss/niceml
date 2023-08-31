"""Module of the SemSeg REST API service"""
import numpy as np
from PIL import Image

from niceml.dagster.ops.prediction import is_numpy_output
from niceml.data.datadescriptions.semsegdatadescritption import SemSegDataDescription
from niceml.deployment.api.rest.rest import RestApi
from niceml.utilities.commonutils import check_instance
from niceml.utilities.encoding import base64_to_bytesio, numpy_to_base64

app = RestApi()


@app.post("/predict")
def predict(input_data: dict):
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
        app.assets["data_description"], SemSegDataDescription
    )
    input_image = input_image.resize(data_description.get_input_image_size().to_pil_size())
    prediction = (
        app.assets["model"]
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
