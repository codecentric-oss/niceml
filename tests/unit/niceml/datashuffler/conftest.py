from typing import List

import pytest

from niceml.data.datainfos.clsdatainfo import ClsDataInfo


@pytest.fixture()
def data_info_list() -> List[ClsDataInfo]:
    df_list = [
        ClsDataInfo(
            identifier=f"{i:03d}",
            image_location=f"{i:03d}",
            class_idx=(i % 4),
            class_name=f"{i:03d}",
        )
        for i in range(20)
    ]
    return df_list
