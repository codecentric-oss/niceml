from collections import defaultdict
from typing import Dict, List

import pytest

from niceml.data.datainfos.clsdatainfo import ClsDataInfo
from niceml.data.datashuffler.datashuffler import DataShuffler
from niceml.data.datashuffler.uniformdistributionshuffler import (
    UniformDistributionShuffler,
)


@pytest.fixture(params=["max", "min", "avg"])
def mode(request) -> str:
    return request.param


@pytest.fixture()
def datashuffler(mode) -> DataShuffler:
    return UniformDistributionShuffler("class_idx", mode=mode)


def test_uniform_dist(
    datashuffler: DataShuffler, data_info_list: List[ClsDataInfo], mode: str
):
    """Test if all classes are uniformly distributed"""
    class_dict: Dict[int, int] = {
        idx: x.get_index_list()[0] for idx, x in enumerate(data_info_list)
    }
    shuffle_idxes = datashuffler.shuffle(data_info_list)
    class_count_dict: Dict[int, int] = defaultdict(int)
    for idx in shuffle_idxes:
        class_count_dict[class_dict[idx]] += 1

    assert len(set(list(class_count_dict.values()))) == 1
    if mode == "max":
        assert len(shuffle_idxes) >= len(data_info_list)
    if mode in ["min", "avg"]:
        assert len(shuffle_idxes) <= len(data_info_list)
