from os.path import join
from tempfile import TemporaryDirectory
from typing import List

import fastparquet
import pandas as pd
import pytest
from attr import asdict

from niceml.data.dataiterators.boundingboxdataiterator import (
    BoundingBoxIterator,
    ObjDetPredictionContainer,
)
from niceml.utilities.boundingboxes.boundingbox import BoundingBox


@pytest.fixture
def image_ids() -> List[str]:
    return ["01.png", "02.png", "03.png", "04.png"]


@pytest.fixture()
def tmp_path() -> str:
    with TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture()
def pred_cols() -> List[str]:
    return [f"pred_{x:04d}" for x in range(5)]


@pytest.fixture()
def target_bbox() -> BoundingBox:
    return BoundingBox(0, 0, 20, 30)


@pytest.fixture()
def parq_file(
    image_ids: List[str], tmp_path: str, pred_cols: List[str], target_bbox: BoundingBox
) -> str:
    df_dict_list: List[dict] = []
    for det_index in range(5):
        cur_bbox_row = dict(image_filepath=image_ids[0], detection_index=det_index)
        cur_bbox_row.update(asdict(target_bbox))
        for pred_idx, pred_col in enumerate(pred_cols):
            cur_bbox_row[pred_col] = float(pred_idx == (det_index % len(pred_cols)))
        df_dict_list.append(cur_bbox_row)

    for cur_id in image_ids[1:]:
        cur_bbox_row = dict(image_filepath=cur_id, detection_index=-1)
        bbox: BoundingBox = BoundingBox(0, 0, 0, 0)
        cur_bbox_row.update(asdict(bbox))
        for pred_idx, pred_col in enumerate(pred_cols):
            cur_bbox_row[pred_col] = 0.0
        df_dict_list.append(cur_bbox_row)

    data_frame = pd.DataFrame(df_dict_list)
    parq_file_path = join(tmp_path, "test")
    fastparquet.write(parq_file_path + ".parq", data_frame)

    return parq_file_path


def test_boundingboxiterator(
    image_ids: List[str], parq_file: str, pred_cols: List[str], target_bbox: BoundingBox
):
    bbox_iterator = BoundingBoxIterator()
    bbox_iterator.open(parq_file)
    data_keys = list(bbox_iterator)
    assert data_keys == image_ids
    for idx, data_key in enumerate(data_keys):
        targets = bbox_iterator[data_key]
        if idx == 0:
            assert len(targets) > 0
            pred_container: ObjDetPredictionContainer
            for pred_container in targets:
                cur_bbox = pred_container.bounding_box
                assert cur_bbox == target_bbox
        else:
            assert len(targets) == 0
