from typing import List

import pytest

from niceml.data.datainfos.clsdatainfo import ClsDataInfo
from niceml.data.datashuffler.datashuffler import DataShuffler
from niceml.data.datashuffler.defaultshuffler import DefaultDataShuffler
from niceml.data.datashuffler.uniformdistributionshuffler import (
    UniformDistributionShuffler,
)


@pytest.fixture(params=["default", "uniform"])
def datashuffler(request) -> DataShuffler:
    if request.param == "uniform":
        return UniformDistributionShuffler("class_idx")
    return DefaultDataShuffler()


def test_randomness(datashuffler: DataShuffler, data_info_list: List[ClsDataInfo]):
    """Checks if the indexes are shuffled"""
    result_idxs = datashuffler.shuffle(data_info_list)
    comparisons = [x != y for x, y in zip(result_idxs, range(len(data_info_list)))]
    assert any(comparisons)


def test_twice_randomness(
    datashuffler: DataShuffler, data_info_list: List[ClsDataInfo]
):
    """Checks if the returned list is not the same"""
    result_idxs = datashuffler.shuffle(data_info_list)
    result_idxs2 = datashuffler.shuffle(data_info_list)
    comparisons = [x != y for x, y in zip(result_idxs, result_idxs2)]
    assert any(comparisons)
