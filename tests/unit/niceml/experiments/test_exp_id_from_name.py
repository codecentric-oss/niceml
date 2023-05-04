from typing import Optional

import pytest

from niceml.experiments.experimentinfo import ExpIdNotFoundError, get_exp_id_from_name


@pytest.mark.parametrize(
    "input_name,target",
    [
        (
            "CLM-2022-05-09T08.40.12.992Z-id_wx9v/models/model-id_wx9v-ep001.hdf5",
            "wx9v",
        ),
        ("prod_models/defectclassificationmodel/model-id_m5vn.hdf5", "m5vn"),
        ("models/prod_model_test.hdf5", None),
        ("test_id_5sdf/model.hdf5", None),
        ("model_id_12", None),
        ("model_id_12/.-", None),
    ],
)
def test_get_exp_id_from_name(input_name: str, target: Optional[str]):
    try:
        pred_id = get_exp_id_from_name(input_name)
        assert pred_id == target
    except ExpIdNotFoundError:
        assert target is None
