import datetime
from typing import Union

import pytest

from niceml.experiments.experimenterrors import (
    MultipleExperimentFoundError,
    ExperimentNotFoundError,
)
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.experiments.exppathfinder import get_exp_filepath
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    open_location,
    join_fs_path,
    join_location_w_path,
)
from niceml.utilities.ioutils import write_yaml


@pytest.fixture
def exp_location(
    tmp_dir,
) -> LocationConfig:
    location_config = LocationConfig(uri=tmp_dir)
    exp_ids = ["abcd", "efgh", "efgh"]
    test_prefix = "TEST"
    with open_location(location_config) as (exps_fs, exps_root):
        for exp_id in exp_ids:
            date = datetime.datetime.utcnow()
            date_string = date.strftime("%Y-%m-%dT%H.%M.%S.%fZ")
            exp_filepath = join_fs_path(
                exps_fs, exps_root, f"{test_prefix}-{date_string}-id_{exp_id}"
            )
            exps_fs.mkdir(exp_filepath)
            exp_info = ExperimentInfo(
                experiment_prefix=test_prefix,
                experiment_name="test",
                experiment_type="",
                run_id=date_string,
                short_id=exp_id,
                environment={},
                description="",
                exp_dir="",
            )
            with open_location(join_location_w_path(location_config, exp_filepath)) as (
                exp_fs,
                exp_root,
            ):
                write_yaml(
                    data=exp_info.as_save_dict(),
                    filepath=join_fs_path(
                        exp_fs, exp_root, ExperimentFilenames.EXP_INFO
                    ),
                )

    return location_config


@pytest.mark.parametrize(
    "exp_id,expected",
    [
        ("abcd", "abcd"),
        ("efgh", MultipleExperimentFoundError),
        ("ijkl", ExperimentNotFoundError),
    ],
)
def test_get_exp_filepath(exp_location, exp_id: str, expected: Union[str, Exception]):
    if isinstance(expected, type):
        with pytest.raises(expected):
            get_exp_filepath(fs_path_config=exp_location, exp_id=exp_id)
    else:
        exp_filepath = get_exp_filepath(fs_path_config=exp_location, exp_id=exp_id)

        assert expected == exp_filepath[-4:]
