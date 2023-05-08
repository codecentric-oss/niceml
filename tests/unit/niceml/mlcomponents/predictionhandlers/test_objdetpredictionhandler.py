from os.path import join
from typing import List

import numpy as np
import pytest

from niceml.data.datadescriptions.objdetdatadescription import ObjDetDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputObjDetDataDescription,
)
from niceml.data.datainfos.objdetdatainfo import ObjDetDataInfo
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.mlcomponents.predictionhandlers.objdetpredictionhandler import (
    ObjDetPredictionHandler,
)
from niceml.utilities.boundingboxes.filtering.nmsfilter import NmsFilter
from niceml.utilities.commonutils import check_instance
from niceml.utilities.fsspec.locationutils import join_location_w_path
from niceml.utilities.imagesize import ImageSize


@pytest.fixture()
def objdet_prediction_handler(tmp_dir: str) -> ObjDetPredictionHandler:
    classes = ["1", "2", "3"]
    img_size = ImageSize(1024, 1024)
    filename = "test"
    data_description = ObjDetDataDescription(
        featuremap_scales=[8, 16, 32, 64, 128],
        classes=classes,
        input_image_size=img_size,
        anchor_aspect_ratios=[1, 0.5, 2.0],
        anchor_scales=[1, 1.25, 1.6],
        anchor_base_area_side=4,
        box_variance=[1.0, 1.0, 2.0, 2.0],
    )
    prediction_filter = NmsFilter()
    prediction_filter.initialize(data_description)
    prediction_handler = ObjDetPredictionHandler(
        apply_sigmoid=False, prediction_filter=prediction_filter
    )
    exp_context = ExperimentContext(
        fs_config={"uri": tmp_dir}, run_id="test", short_id="test"
    )
    prediction_handler.set_params(
        data_description=data_description, filename=filename, exp_context=exp_context
    )
    prediction_handler.initialize()
    return prediction_handler


@pytest.mark.parametrize(
    "predictions, target_cols",
    [
        (
            np.array(
                [
                    np.array(
                        [
                            np.array(
                                [
                                    0.423828125,
                                    0.5927734375,
                                    0.478515625,
                                    0.6416015625,
                                    0.0,
                                    0.0,
                                    0.0,
                                ]
                            ),
                            np.array(
                                [
                                    0.413828125,
                                    0.5827734375,
                                    0.468515625,
                                    0.6316015625,
                                    0.0,
                                    0.0,
                                    0.0,
                                ]
                            ),
                        ]
                    )
                ]
            ),
            [
                "image_location",
                "detection_index",
                "x_pos",
                "y_pos",
                "width",
                "height",
                "pred_0000",
                "pred_0001",
                "pred_0002",
            ],
        )
    ],
)
def test_objdet_prediction_handler(
    predictions: np.ndarray,
    target_cols: List[str],
    objdet_prediction_handler: ObjDetPredictionHandler,
):
    location = objdet_prediction_handler.exp_context.fs_config
    filename = objdet_prediction_handler.filename
    output_dd: OutputObjDetDataDescription = check_instance(
        objdet_prediction_handler.data_description, OutputObjDetDataDescription
    )
    class_count = output_dd.get_output_class_count()
    anchor_count = 196416

    data_info_list: List[ObjDetDataInfo] = [
        ObjDetDataInfo(
            image_location=join_location_w_path(location, filename),
            labels=[],
            class_count_in_dataset=class_count,
        )
    ]

    predictions = np.expand_dims(
        np.array([predictions[0, index % 2] for index in range(anchor_count)]), axis=0
    )

    predictions[0, 1, 4:] = [0.2, 0.3, 0.4]
    predictions[0, 100, 4:] = [0.2, 0.3, 0.4]
    predictions[0, 200, 4:] = [0.2, 0.3, 0.4]
    predictions[0, 1000, 4:] = [0.2, 0.3, 0.4]
    predictions[0, 2000, 4:] = [0.2, 0.3, 0.4]
    with objdet_prediction_handler as prediction_handler:
        prediction_handler.add_prediction(
            data_info_list=data_info_list, prediction_batch=predictions
        )

    pred_dataframe = objdet_prediction_handler.exp_context.read_parquet(
        join(ExperimentFilenames.PREDICTION_FOLDER, filename + ".parq"),
    )

    assert list(pred_dataframe.columns) == target_cols
