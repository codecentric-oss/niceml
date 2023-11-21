from typing import List, Tuple

import numpy as np
import pytest
from numpy.random import Generator

from niceml.data.datadescriptions.semsegdatadescritption import (
    SemSegClassInfo,
    SemSegDataDescription,
)
from niceml.mlcomponents.predictionhandlers.semsegpredictionhandler import (
    create_bbox_prediction_from_mask_instances,
)
from niceml.mlcomponents.resultanalyzers.instancefinders.maskinstance import (
    MaskInstance,
)
from niceml.mlcomponents.resultanalyzers.instancefinders.multichannelinstancefinder import (
    MultiChannelInstanceFinder,
)
from niceml.mlcomponents.resultanalyzers.tensors.semsegdataiterator import (
    SemSegPredictionContainer,
)
from niceml.utilities.imagesize import ImageSize
from tests.unit.niceml.utilities.semseg.testutils import get_random_semseg_mask


@pytest.fixture()
def image_shape() -> Tuple[int, int]:
    return 1024, 1024


@pytest.fixture()
def random_generator() -> Generator:
    random_generator = np.random.default_rng(seed=42)

    return random_generator


@pytest.fixture()
def class_list() -> List[str]:
    return ["0", "1", "2"]


@pytest.fixture()
def random_mask_instances(
    image_shape, random_generator, class_list
) -> List[MaskInstance]:
    instance_finder = MultiChannelInstanceFinder()
    class_infos = [
        SemSegClassInfo(color=[], name=class_name) for class_name in class_list
    ]
    data_description = SemSegDataDescription(
        classes=class_infos,
        input_image_size=ImageSize(*image_shape),
        output_image_size=ImageSize(*image_shape),
    )
    instance_finder.initialize(
        data_description=data_description, exp_context=None, dataset_name="test"
    )

    idx_mask, pred_mask = get_random_semseg_mask(
        image_shape=image_shape,
        random_generator=random_generator,
        class_list=class_list,
        square_width=50,
        square_height=50,
    )

    prediction_container = SemSegPredictionContainer(
        max_prediction_idxes=idx_mask, max_prediction_values=pred_mask
    )
    instances = instance_finder.analyse_datapoint(
        "", data_predicted=prediction_container
    )
    return instances


@pytest.mark.parametrize("target_coords", [[(427, 637, 50, 50), (836, 421, 50, 50)]])
def test_create_bbox_prediction_from_mask_instances(
    random_mask_instances,
    image_shape,
    random_generator,
    class_list,
    target_coords: List[List[int]],
):
    prediction = random_generator.uniform(
        low=0.5, high=1.0, size=(image_shape[0], image_shape[1], len(class_list))
    )

    bbox_predictions = create_bbox_prediction_from_mask_instances(
        prediction=prediction, mask_instances=random_mask_instances
    )

    for pred, target in zip(bbox_predictions, target_coords):
        assert target == tuple(pred[1][:4])


@pytest.mark.parametrize("box_size", [4, 1, 2, 3])
def test_create_bbox_prediction_from_mask_instances_small_box_size(
    box_size: int, class_list
):
    mask = np.zeros(shape=(32, 32, 3))
    mask[5 : 5 + box_size, 10 : 10 + box_size, 1] = 0.6
    instance_finder = MultiChannelInstanceFinder(min_area=0, max_area=10000000)
    prediction_container = SemSegPredictionContainer(
        max_prediction_idxes=np.argmax(mask, axis=2),
        max_prediction_values=np.max(mask, axis=2),
    )
    instances = instance_finder.analyse_datapoint(
        "", data_predicted=prediction_container
    )

    bbox_predictions = create_bbox_prediction_from_mask_instances(
        prediction=mask, mask_instances=instances
    )
    bbox_prediction = bbox_predictions[0][1]
    assert bbox_prediction[0] == 10.0
    assert bbox_prediction[1] == 5.0
    assert bbox_prediction[2] == box_size
    assert bbox_prediction[3] == box_size
    assert len(bbox_prediction) == 4 + len(class_list)
