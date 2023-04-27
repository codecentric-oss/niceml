from os.path import join

import pandas as pd
import pytest

from niceml.utilities.ioutils import read_parquet, write_parquet


@pytest.fixture
def data() -> pd.DataFrame:
    data_list = [{"a": x, "b": x**2, "c": x**3, "d": [1, x, 3]} for x in range(10)]
    data_frame = pd.DataFrame(data_list)
    return data_frame


def test_parquet_io(tmp_dir: str, data: pd.DataFrame):
    parq_file = join(tmp_dir, "data.parq")
    write_parquet(data, parq_file)
    loaded_data = read_parquet(parq_file)
    assert loaded_data.equals(data)
