import pytest

from niceml.mlcomponents.resultanalyzers.tensors.tensorgraphanalyzer import (
    metrics_dict_to_mlflow_metrics_dict,
)


@pytest.mark.parametrize(
    "input_metrics, expected_output",
    [
        (
            {
                "accuracy": 0.85,
                "precision": {"class_0": 0.90, "class_1": 0.78},
                "loss": [0.5, 0.3, 0.2],
                "confusion_matrix": [[50, 5], [10, 80]],
            },
            {
                "accuracy": 0.85,
                "precision_class_0": 0.90,
                "precision_class_1": 0.78,
                "loss_0": 0.5,
                "loss_1": 0.3,
                "loss_2": 0.2,
                "confusion_matrix_0_0": 50.0,
                "confusion_matrix_0_1": 5.0,
                "confusion_matrix_1_0": 10.0,
                "confusion_matrix_1_1": 80.0,
            },
        ),
        (
            {
                "accuracy": 0.95,
                "precision": {"class_A": 0.88, "class_B": 0.92},
                "f1_score": [0.91, 0.93],
                "recall": {"class_X": 0.85, "class_Y": 0.78},
            },
            {
                "accuracy": 0.95,
                "precision_class_A": 0.88,
                "precision_class_B": 0.92,
                "f1_score_0": 0.91,
                "f1_score_1": 0.93,
                "recall_class_X": 0.85,
                "recall_class_Y": 0.78,
            },
        ),
        (
            {
                "metric1": 42.0,
                "metric2": {"type_A": 10, "type_B": 20},
                "metric3": [1, 2, 3],
                "metric4": [[1, 2], [3, 4]],
            },
            {
                "metric1": 42.0,
                "metric2_type_A": 10,
                "metric2_type_B": 20,
                "metric3_0": 1.0,
                "metric3_1": 2.0,
                "metric3_2": 3.0,
                "metric4_0_0": 1.0,
                "metric4_0_1": 2.0,
                "metric4_1_0": 3.0,
                "metric4_1_1": 4.0,
            },
        ),
    ],
)
def test_metrics_dict_to_mlflow_metrics_dict_success(input_metrics, expected_output):
    result = metrics_dict_to_mlflow_metrics_dict(input_metrics)
    assert result == expected_output


@pytest.mark.parametrize(
    "input_metrics",
    [
        {
            "accuracy": 1,  # int
            "precision": {"class_0": 0.90, "class_1": 0.78},
            "loss": [0.5, 0.3, 0.2],
            "confusion_matrix": [[50, 5], [10, 80]],
        },
        {
            "accuracy": 0.85,
            "precision": {"class_0": 0.90, "class_1": 0.78},
            "loss": (0.5, 0.2),  # tuple
            "confusion_matrix": [[50, 5], [10, 80]],
        },
    ],
)
def test_metrics_dict_to_mlflow_metrics_dict_exception(input_metrics: dict):
    with pytest.raises(ValueError):
        metrics_dict_to_mlflow_metrics_dict(input_metrics)
        assert True
