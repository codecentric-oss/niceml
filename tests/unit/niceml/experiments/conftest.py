from os.path import dirname, join
from tempfile import TemporaryDirectory

import pandas as pd
import pytest
import yaml

from niceml.experiments.experimentcontext import ExperimentContext
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.experiments.expoutinitializer import produce_exp_info


@pytest.fixture()
def tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture()
def exp_info_path(tmp_dir) -> str:
    return join(tmp_dir, ExperimentFilenames.EXP_INFO)


@pytest.fixture()
def exp_info_data(exp_info_path: str, experiment_data: ExperimentData) -> dict:
    exp_info: ExperimentInfo = experiment_data.exp_info
    exp_context = ExperimentContext(
        fs_config=dict(uri=dirname(exp_info_path)),
        run_id=exp_info.run_id,
        short_id=exp_info.short_id,
    )

    produce_exp_info(
        exp_context=exp_context,
        filepath=ExperimentFilenames.EXP_INFO,
        environment=exp_info.environment,
        description=exp_info.description,
        short_id=exp_info.short_id,
        run_id=exp_info.run_id,
        exp_name=exp_info.experiment_name,
        exp_prefix=exp_info.experiment_prefix,
    )
    with open(exp_info_path, "r", encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)

    return data


@pytest.fixture
def experiment_data() -> ExperimentData:
    run_id = "2022-05-05T14.17.18.287Z"
    exp_info = ExperimentInfo(
        experiment_name="exp_name",
        experiment_prefix="PREFIX",
        experiment_type="TEST",
        run_id=run_id,
        short_id="hnk0",
        environment=dict(DATATYPE="sample"),
        description="No description",
        exp_dir=f"PREFIX-{run_id}-id_hnk0",
    )
    data_train_conf = {
        "_target_": "ccmlops.datasets.imageclsdata.ImageClsDataGenerator",
        "batch_size": 16,
        "image_location": "data/classification",
    }
    config_data = {
        "data_train": data_train_conf,
        "image_size": {
            "_target_": "niceml.utils.ImageSize",
            "width": 256,
            "height": 256,
        },
    }
    log_list = [
        dict(epoch=0, loss=1.0, val_loss=1.1),
        dict(epoch=1, loss=0.9, val_loss=1.0),
        dict(epoch=2, loss=0.8, val_loss=0.9),
    ]
    return ExperimentData(
        dir_name="test_folder_name",
        exp_info=exp_info,
        log_data=pd.DataFrame(log_list),
        exp_dict_data={"configs/datasets": config_data},
        exp_files=[],
    )
