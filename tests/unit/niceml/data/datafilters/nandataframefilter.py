import pytest
import pandas as pd
from niceml.data.datadescriptions.regdatadescription import RegDataDescription
from niceml.data.datafilters.nandataframefilter import NanDataframeFilter


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {"A": [1, 2, 3, pd.NA], "B": [4, pd.NA, 6, 7], "C": [8, 9, 10, 11]}
    )


@pytest.fixture
def sample_data_description():
    return RegDataDescription(
        inputs=[{"key": "A"}, {"key": "B"}], targets=[{"key": "C"}]
    )


@pytest.mark.parametrize(
    "input_data, data_description, expected_data",
    [
        (
            pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}),
            RegDataDescription(inputs=[{"key": "A"}], targets=[{"key": "C"}]),
            pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}),
        ),
        (
            pd.DataFrame({"A": [1, pd.NA, 3], "B": [4, 5, 6], "C": [7, 8, 9]}),
            RegDataDescription(
                inputs=[{"key": "A"}, {"key": "B"}], targets=[{"key": "C"}]
            ),
            pd.DataFrame({"A": [1, 3], "B": [4, 6], "C": [7, 9]}),
        ),
    ],
)
def test_nan_dataframe_filter(input_data, data_description, expected_data):
    nan_filter = NanDataframeFilter()
    nan_filter.initialize(data_description)
    filtered_data = nan_filter.filter(input_data)
    filtered_data = filtered_data.reset_index(drop=True)
    assert all(filtered_data == expected_data)
