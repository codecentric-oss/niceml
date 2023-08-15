import os
from os.path import join
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

import pytest
import yaml

import niceml
from niceml.dagster.jobs.jobs import job_data_generation, job_eval, job_train
from niceml.data.dataloaders.dfloaders import SimpleDfLoader
from niceml.data.dataloaders.imageloaders import SimpleImageLoader
from niceml.data.storages.localstorage import LocalStorage
from niceml.experiments.expdatastorageloader import create_expdata_from_storage
from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimentinfo import ExperimentInfo


@pytest.fixture(scope="session")
def tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture(scope="session")
def trainregression(tmp_dir: str):
    os.environ["EXPERIMENT_URI"] = tmp_dir
    os.environ["EPOCHS"] = "1"
    config_path = (
        Path(niceml.__file__).parent.parent
        / "configs"
        / "jobs"
        / "job_train"
        / "job_train_reg"
        / "job_train_reg_number.yaml"
    )
    print(f"job to test: {job_train.name}")
    config = yaml.load(config_path.read_text(encoding="utf-8"), Loader=yaml.SafeLoader)
    job_train.execute_in_process(run_config=config)
    return tmp_dir


@pytest.fixture(scope="session")
def load_experiment(trainregression: str) -> ExperimentData:
    exp_storage = LocalStorage(trainregression)
    exp_info_list: List[ExperimentInfo] = exp_storage.list_experiments()
    exp_filepath = exp_info_list[0].exp_filepath
    df_loader = SimpleDfLoader(working_dir=join(trainregression, exp_filepath))
    image_loader = SimpleImageLoader(working_dir=join(trainregression, exp_filepath))
    exp_data: ExperimentData = create_expdata_from_storage(
        exp_filepath, exp_storage, df_loader=df_loader, image_loader=image_loader
    )
    return exp_data


@pytest.fixture(scope="session")
def eval_regression(trainregression: str):
    os.environ["EXPERIMENT_URI"] = trainregression
    os.environ["EPOCHS"] = "1"
    config_path = (
        Path(niceml.__file__).parent.parent
        / "configs"
        / "jobs"
        / "job_eval"
        / "job_eval_reg"
        / "job_eval_reg_number.yaml"
    )
    print(f"job to test: {job_eval.name}")
    config = yaml.load(config_path.read_text(encoding="utf-8"), Loader=yaml.SafeLoader)
    job_eval.execute_in_process(run_config=config)
    return trainregression


@pytest.fixture(scope="session")
def load_eval_experiment(eval_regression: str):
    exp_storage = LocalStorage(eval_regression)
    exp_info_list: List[ExperimentInfo] = exp_storage.list_experiments()
    exp_info_list = sorted(exp_info_list, key=lambda x: x.run_id)
    assert len(exp_info_list) == 2
    exp_filepath = exp_info_list[1].exp_filepath
    df_loader = SimpleDfLoader(working_dir=join(eval_regression, exp_filepath))
    image_loader = SimpleImageLoader(working_dir=join(eval_regression, exp_filepath))
    exp_data: ExperimentData = create_expdata_from_storage(
        exp_filepath,
        exp_storage,
        df_loader=df_loader,
        image_loader=image_loader,
    )
    return exp_data


@pytest.fixture(scope="session")
def experiment_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture(scope="session")
def data_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture(scope="session")
def sample_count() -> int:
    return 60


@pytest.fixture(scope="session")
def generate_number_data(data_dir: str, sample_count: int) -> str:
    os.environ["SAMPLE_COUNT"] = f"{sample_count}"
    os.environ["DATA_URI"] = data_dir
    os.environ["MAX_NUMBER"] = "3"
    config_path = (
        Path(niceml.__file__).parent.parent
        / "configs"
        / "jobs"
        / "job_data_generation"
        / "job_data_generation.yaml"
    )
    config = yaml.load(config_path.read_text(encoding="utf-8"), Loader=yaml.SafeLoader)
    job_data_generation.execute_in_process(run_config=config)
    return data_dir


@pytest.fixture()
def obj_det_split_dir(generate_number_data: str) -> str:
    return join(generate_number_data, "number_data_split")


@pytest.fixture()
def numbers_cropped_split_dir(generate_number_data: str) -> str:
    return join(generate_number_data, "numbers_cropped_split")
