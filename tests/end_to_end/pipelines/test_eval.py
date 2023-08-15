from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentinfo import get_exp_id_from_name
from niceml.experiments.schemas.sampleexpschemas import NumRegExpSchema
from niceml.experiments.schemas.schemavalidation import validate_schema


def test_exp_eval_regression_data(load_eval_experiment: ExperimentData):
    result = validate_schema(load_eval_experiment, NumRegExpSchema)
    assert result
    model_id: str = get_exp_id_from_name(load_eval_experiment.get_all_model_files()[0])
    exp_id = load_eval_experiment.get_short_id()
    # the model id and exp_id must be different
    # because the model was trained in a different exp
    assert model_id != exp_id
