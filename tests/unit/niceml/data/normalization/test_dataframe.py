import pytest
import pandas as pd

from niceml.data.normalization.dataframe import normalize_scalar_col
from niceml.data.normalization.normalization import NormalizationInfo


@pytest.fixture
def sample_dataframe():
    data = {"column1": [1, 2, 3, 4, 5], "column2": [10, 20, 30, 40, 50]}
    return pd.DataFrame(data)


@pytest.mark.parametrize(
    "column_key, expected_output, expected_norm_info",
    [
        (
            "column1",
            pd.DataFrame(
                {
                    "column1": [0.0, 0.25, 0.5, 0.75, 1.0],
                    "column2": [10, 20, 30, 40, 50],
                }
            ),
            NormalizationInfo(feature_key="column1", offset=1.0, divisor=4.0),
        ),
        (
            "column2",
            pd.DataFrame(
                {"column1": [1, 2, 3, 4, 5], "column2": [0.0, 0.25, 0.5, 0.75, 1.0]}
            ),
            NormalizationInfo(feature_key="column2", offset=10.0, divisor=40.0),
        ),
    ],
)
def test_normalize_col(
    sample_dataframe, column_key, expected_output, expected_norm_info
):
    input_dataframe = sample_dataframe.copy()

    output_dataframe, norm_info = normalize_scalar_col(input_dataframe, column_key)

    assert output_dataframe.equals(expected_output)
    assert norm_info.feature_key == expected_norm_info.feature_key
    assert norm_info.offset == expected_norm_info.offset
    assert norm_info.divisor == expected_norm_info.divisor
