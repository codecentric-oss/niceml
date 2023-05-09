"""Run all jobs sequentially with test configuration."""
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.schemas.sampleexpschemas import SinRegExpSchema
from niceml.experiments.schemas.schemavalidation import validate_schema


def test_exp_regression_data(load_experiment: ExperimentData):
    result = validate_schema(load_experiment, SinRegExpSchema)
    assert result
