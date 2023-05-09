import pytest

from niceml.config.envconfig import EXP_NAME_KEY, EXP_PREFIX_KEY, EXP_TYPE_KEY
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.metafunctions import (
    EpochsExtractor,
    ExperimentIdExtraction,
    ExperimentInfoExtraction,
)


def test_experiment_id_extraction(experiment_data):
    func = ExperimentIdExtraction()
    pred = func(experiment_data)
    assert pred == "hnk0"


def test_epochs_extractor(experiment_data):
    func = EpochsExtractor()
    pred = func(experiment_data)
    assert pred == 3


@pytest.mark.parametrize(
    "key,target",
    [(EXP_TYPE_KEY, "TEST"), (EXP_PREFIX_KEY, "PREFIX"), (EXP_NAME_KEY, "exp_name")],
)
def test_exp_info_extractor(key: str, target: str, experiment_data: ExperimentData):
    func = ExperimentInfoExtraction("test", key)
    pred = func(experiment_data)
    assert pred == target
