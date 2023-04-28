"""Module for loading experiment info"""
from niceml.data.storages.storageinterface import StorageInterface
from niceml.experiments.experimentinfo import ExperimentInfo, experiment_info_factory
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.experiments.loaddatafunctions import LoadYamlFile


def load_exp_info(storage: StorageInterface, exp_path: str) -> ExperimentInfo:
    """Loads the experiment info file"""
    if len(exp_path) == 0:
        target_path = ExperimentFilenames.EXP_INFO
    else:
        target_path = storage.join_paths(exp_path, ExperimentFilenames.EXP_INFO)
    yaml_data = LoadYamlFile().load_data(target_path, storage)
    if yaml_data is None:
        raise FileNotFoundError(f"Info File {exp_path} is empty!")
    return experiment_info_factory(yaml_data, path=exp_path)
