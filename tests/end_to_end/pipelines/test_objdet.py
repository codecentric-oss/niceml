import os
from os.path import join
from pathlib import Path
from typing import List

import pytest
import yaml

import niceml
from niceml.dagster.jobs.jobs import job_train
from niceml.data.dataloaders.dfloaders import SimpleDfLoader
from niceml.data.dataloaders.imageloaders import SimpleImageLoader
from niceml.data.storages.localstorage import LocalStorage
from niceml.experiments.expdatastorageloader import create_expdata_from_storage
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentinfo import ExperimentInfo
from niceml.experiments.schemas.objdetexpschema import ObjDetExpSchema
from niceml.experiments.schemas.schemavalidation import validate_schema


# pylint: disable = duplicate-code
@pytest.fixture(scope="module")
def train_objdet(generate_number_data: str, experiment_dir: str) -> str:
    os.environ["EXPERIMENT_URI"] = experiment_dir
    os.environ["TRAINING_EPOCHS"] = "1"
    os.environ["STEPS_PER_EPOCH"] = "2"
    os.environ["VALIDATION_STEPS"] = "2"
    os.environ["PREDICTION_STEPS"] = "3"
    config_path = (
        Path(niceml.__file__).parent.parent
        / "configs"
        / "jobs"
        / "job_train"
        / "job_train_objdet"
        / "job_train_objdet_number.yaml"
    )
    print(f"job to test: {job_train.name}")
    config = yaml.load(config_path.read_text(encoding="utf-8"), Loader=yaml.SafeLoader)
    job_train.execute_in_process(run_config=config)
    return experiment_dir


@pytest.fixture(scope="module")
def load_experiment_objdet(train_objdet):
    exp_storage = LocalStorage(train_objdet)
    exp_info_list: List[ExperimentInfo] = exp_storage.list_experiments()
    exp_filepath = exp_info_list[0].exp_filepath
    df_loader = SimpleDfLoader(working_dir=join(train_objdet, exp_filepath))
    image_loader = SimpleImageLoader(working_dir=join(train_objdet, exp_filepath))
    exp_data: ExperimentData = create_expdata_from_storage(
        exp_filepath, exp_storage, df_loader=df_loader, image_loader=image_loader
    )
    return exp_data


def test_train_objdet(load_experiment_objdet: ExperimentData):
    result = validate_schema(load_experiment_objdet, ObjDetExpSchema)
    assert result
