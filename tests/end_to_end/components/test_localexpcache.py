from tempfile import TemporaryDirectory

import pytest

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.localexperimentcache import (
    LocalExperimentCache,
    ExperimentCache,
)
from niceml.utilities.timeutils import generate_timestamp


@pytest.fixture()
def local_exp_cache() -> ExperimentCache:
    """Factory method for the local experiment cache"""
    with TemporaryDirectory() as tmp_dir:
        yield LocalExperimentCache(tmp_dir)


def test_localexperiment_cache(
    load_eval_experiment: ExperimentData, local_exp_cache: ExperimentCache
):
    assert load_eval_experiment is not None

    assert load_eval_experiment.get_short_id() not in local_exp_cache
    assert local_exp_cache.get_exp_count_in_cache() == 0

    local_exp_cache.save_experiment(load_eval_experiment)
    assert local_exp_cache.get_exp_count_in_cache() == 1

    assert load_eval_experiment.exp_info.short_id in local_exp_cache

    loaded_exp_info = local_exp_cache.load_exp_info(load_eval_experiment.get_short_id())

    assert isinstance(loaded_exp_info, ExperimentInfo)
    assert loaded_exp_info.short_id == load_eval_experiment.get_short_id()

    loaded_exp = local_exp_cache.load_experiment(load_eval_experiment.get_short_id())
    assert isinstance(loaded_exp, ExperimentData)
    assert loaded_exp.get_short_id() == load_eval_experiment.get_short_id()

    assert not local_exp_cache.should_reload(loaded_exp_info)

    # change timestamp
    loaded_exp_info.last_modified = generate_timestamp()
    assert local_exp_cache.should_reload(loaded_exp_info)
