from abc import ABC, abstractmethod
from typing import Any, List, Optional

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimenterrors import InfoNotFoundError


class MetaFunction(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def __call__(self, experiment_data: ExperimentData) -> Any:
        pass


class ExperimentIdExtraction(MetaFunction):
    def __init__(self, name: str = "Id"):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def __call__(self, experiment_data: ExperimentData) -> Any:
        return experiment_data.get_short_id()


class ExperimentInfoExtraction(MetaFunction):
    def __init__(self, name: str, key: str):
        self.name = name
        self.key = key

    def get_name(self) -> str:
        return self.name

    def __call__(self, experiment_data: ExperimentData) -> Any:
        cur_dict = experiment_data.exp_info.as_save_dict()
        if self.key in cur_dict:
            return cur_dict[self.key]
        else:
            return None


class EnvironmentExtractor(MetaFunction):
    def __init__(self, name: str, env_key: str):
        self.name = name
        self.env_key = env_key

    def get_name(self) -> str:
        return self.name

    def __call__(self, experiment_data: ExperimentData) -> Any:
        env_vars: dict = experiment_data.exp_info.environment
        return env_vars.get(self.env_key, None)


class EpochsExtractor(MetaFunction):
    def __init__(self, name: str = "epochs"):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def __call__(self, experiment_data: ExperimentData) -> Any:
        return experiment_data.get_trained_epochs()


class ModelExtractor(MetaFunction):
    def __init__(self, name: str = "model", model_path: Optional[List[str]] = None):
        self.model_path: List[str] = ["model"] if model_path is None else model_path
        self.name = name

    def get_name(self) -> str:
        return self.name

    def __call__(self, experiment_data: ExperimentData):
        try:
            model_info = experiment_data.get_config_information(
                self.model_path + ["_target_"]
            )
            model_name = model_info.rsplit(".", maxsplit=1)[1]
            if model_name == "ClsModelFactory":
                model_info = experiment_data.get_config_information(
                    self.model_path + ["model", "_target_"]
                )
                model_name = model_info.rsplit(".", maxsplit=1)[1]
        except (KeyError, InfoNotFoundError):
            model_name = None
        return model_name
