import pytest
import pandas as pd

from niceml.data.normalization.dataframe import (
    normalize_scalar_column,
    normalize_categorical_column,
    normalize_binary_column,
    denormalize_column,
)
from niceml.data.normalization.normalization import (
    ScalarNormalizationInfo,
    CategoricalNormalizationInfo,
    BinaryNormalizationInfo,
)


@pytest.fixture
def sample_dataframe():
    data = {"column1": [1, 2, 3, 4, 5], "column2": [10, 20, 30, 40, 50]}
    return pd.DataFrame(data)


@pytest.fixture
def sample_scalar_normalized_dataframe():
    data = {
        "column1": [0.0, 0.25, 0.5, 0.75, 1.0],
        "column2": [0.0, 0.25, 0.5, 0.75, 1.0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_categorical_normalized_dataframe():
    data = {"column1": [0, 1, 2, 3, 4], "column2": [0, 1, 2, 3, 4]}
    return pd.DataFrame(data)


@pytest.fixture
def sample_binary_dataframe():
    data = {
        "column1": ["OK", "NOK", "OK", "OK", "NOK"],
        "column2": ["OK", "OK", "OK", "NOK", "OK"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_binary_normalized_dataframe():
    return pd.DataFrame({"column1": [1, 0, 1, 1, 0], "column2": [1, 1, 1, 0, 1]})


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
            ScalarNormalizationInfo(feature_key="column1", offset=1.0, divisor=4.0),
        ),
        (
            "column2",
            pd.DataFrame(
                {"column1": [1, 2, 3, 4, 5], "column2": [0.0, 0.25, 0.5, 0.75, 1.0]}
            ),
            ScalarNormalizationInfo(feature_key="column2", offset=10.0, divisor=40.0),
        ),
    ],
)
def test_normalize_scalar_col(
    sample_dataframe, column_key, expected_output, expected_norm_info
):
    input_dataframe = sample_dataframe.copy()

    output_dataframe, norm_info = normalize_scalar_column(input_dataframe, column_key)

    assert output_dataframe.equals(expected_output)
    assert norm_info.feature_key == expected_norm_info.feature_key
    assert norm_info.offset == expected_norm_info.offset
    assert norm_info.divisor == expected_norm_info.divisor


@pytest.mark.parametrize(
    "column_key, expected_output, expected_norm_info",
    [
        (
            "column2",
            pd.DataFrame({"column1": [1, 2, 3, 4, 5], "column2": [0, 1, 2, 3, 4]}),
            CategoricalNormalizationInfo(
                feature_key="column2", values=[10, 20, 30, 40, 50]
            ),
        ),
        (
            "column1",
            pd.DataFrame({"column1": [0, 1, 2, 3, 4], "column2": [10, 20, 30, 40, 50]}),
            CategoricalNormalizationInfo(feature_key="column1", values=[1, 2, 3, 4, 5]),
        ),
    ],
)
def test_normalize_categorical_col(
    sample_dataframe, column_key, expected_output, expected_norm_info
):
    input_dataframe = sample_dataframe.copy()

    output_dataframe, norm_info = normalize_categorical_column(
        input_dataframe, column_key
    )

    assert output_dataframe.equals(expected_output)
    assert norm_info.feature_key == expected_norm_info.feature_key
    assert norm_info.values == expected_norm_info.values


@pytest.mark.parametrize(
    "column_key, expected_output, expected_norm_info",
    [
        (
            "column1",
            pd.DataFrame(
                {"column1": [1, 0, 1, 1, 0], "column2": ["OK", "OK", "OK", "NOK", "OK"]}
            ),
            BinaryNormalizationInfo(feature_key="column1", values=["NOK", "OK"]),
        ),
        (
            "column2",
            pd.DataFrame(
                {
                    "column1": ["OK", "NOK", "OK", "OK", "NOK"],
                    "column2": [1, 1, 1, 0, 1],
                }
            ),
            BinaryNormalizationInfo(feature_key="column2", values=["NOK", "OK"]),
        ),
    ],
)
def test_normalize_binary_col(
    sample_binary_dataframe, column_key, expected_output, expected_norm_info
):
    input_dataframe = sample_binary_dataframe.copy()

    output_dataframe, norm_info = normalize_binary_column(input_dataframe, column_key)

    assert output_dataframe.equals(expected_output)
    assert norm_info.feature_key == expected_norm_info.feature_key
    assert norm_info.values == expected_norm_info.values


@pytest.mark.parametrize(
    "expected_output,normalization_info",
    [
        (
            pd.DataFrame(
                {
                    "column1": ["OK", "NOK", "OK", "OK", "NOK"],
                    "column2": [1, 1, 1, 0, 1],
                }
            ),
            BinaryNormalizationInfo(feature_key="column1", values=["NOK", "OK"]),
        ),
        (
            pd.DataFrame(
                {"column1": [1, 0, 1, 1, 0], "column2": ["OK", "OK", "OK", "NOK", "OK"]}
            ),
            BinaryNormalizationInfo(feature_key="column2", values=["NOK", "OK"]),
        ),
    ],
)
def test_denormalize_binary_col(
    sample_binary_normalized_dataframe, expected_output, normalization_info
):
    input_dataframe = sample_binary_normalized_dataframe.copy()

    output_dataframe = denormalize_column(
        data=input_dataframe, norm_info=normalization_info
    )

    assert output_dataframe.equals(expected_output)


@pytest.mark.parametrize(
    "expected_output,normalization_info",
    [
        (
            pd.DataFrame({"column1": [1, 2, 3, 4, 5], "column2": [0, 1, 2, 3, 4]}),
            CategoricalNormalizationInfo(feature_key="column1", values=[1, 2, 3, 4, 5]),
        ),
        (
            pd.DataFrame({"column1": [0, 1, 2, 3, 4], "column2": [10, 20, 30, 40, 50]}),
            CategoricalNormalizationInfo(
                feature_key="column2", values=[10, 20, 30, 40, 50]
            ),
        ),
    ],
)
def test_denormalize_categorical_col(
    sample_categorical_normalized_dataframe, expected_output, normalization_info
):
    input_dataframe = sample_categorical_normalized_dataframe.copy()

    output_dataframe = denormalize_column(
        data=input_dataframe, norm_info=normalization_info
    )

    assert output_dataframe.equals(expected_output)


@pytest.mark.parametrize(
    "expected_output,normalization_info",
    [
        (
            pd.DataFrame(
                {
                    "column1": [0.0, 0.25, 0.5, 0.75, 1.0],
                    "column2": [10.0, 20.0, 30.0, 40.0, 50.0],
                }
            ),
            ScalarNormalizationInfo(feature_key="column2", offset=10.0, divisor=40.0),
        ),
        (
            pd.DataFrame(
                {
                    "column1": [1.0, 2.0, 3.0, 4.0, 5.0],
                    "column2": [0.0, 0.25, 0.5, 0.75, 1.0],
                }
            ),
            ScalarNormalizationInfo(feature_key="column1", offset=1.0, divisor=4.0),
        ),
    ],
)
def test_denormalize_scalar_col(
    sample_scalar_normalized_dataframe, expected_output, normalization_info
):
    input_dataframe = sample_scalar_normalized_dataframe.copy()

    output_dataframe = denormalize_column(
        data=input_dataframe, norm_info=normalization_info
    )

    assert output_dataframe.equals(expected_output)
