"""modules for configinfoextractor"""
from typing import Callable, List, Optional, Union

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.experimenterrors import InfoNotFoundError
from niceml.experiments.metafunctions import MetaFunction


class ConfigInfoExtractor(MetaFunction):
    """Extracts information from ExperimentData"""

    def __init__(
        self,
        name: str,
        info_path: Union[List[Union[str, int]], List[List[Union[str, int]]]],
        info_format_func: Optional[Callable] = None,
        use_yaml_files: bool = False,
    ):
        self.name = name
        self.info_path_list: List[List[Union[str, int]]] = (
            info_path if isinstance(info_path[0], list) else [info_path]
        )
        self.info_format_func = info_format_func
        self.use_yaml_files = use_yaml_files

    def get_name(self) -> str:
        return self.name

    def __call__(self, experiment_data: ExperimentData):
        info = None
        for info_path in self.info_path_list:
            try:
                if self.use_yaml_files:
                    info = experiment_data.get_yaml_information(info_path)
                else:
                    info = experiment_data.get_config_information(info_path)
            except (KeyError, InfoNotFoundError):
                continue
            if info is not None:
                break
        if self.info_format_func is not None and info is not None:
            info = self.info_format_func(info)
        return info


class DictKeysToStringFormatFunc:  # pylint: disable=too-few-public-methods
    """Extracts the given key list from the dictionary"""

    def __init__(self, key_list: List[str], join_str: str = "x"):
        self.key_list = key_list
        self.join_str = join_str

    def __call__(self, input_dict: Union[dict, str, None]) -> Optional[str]:
        if input_dict is None or isinstance(input_dict, str):
            return input_dict
        out_list: List[str] = []
        for key in self.key_list:
            if key in input_dict:
                out_list.append(str(input_dict[key]))
        if len(out_list) > 0:
            return self.join_str.join(out_list)
        return None


def git_hashtag_shortener(hashtag: Union[str, bytes, None]):
    """Return a 6-digit hashtag"""
    if hashtag is None:
        return None
    if isinstance(hashtag, bytes):
        hashtag = hashtag.decode("utf-8")
    return hashtag[:6]


def list_to_str_format_func(input_list: Union[list, str, None]) -> Optional[str]:
    """Concatenates a list of str joined with a comma"""
    if input_list is None:
        return None
    if isinstance(input_list, str):
        return input_list
    str_list = [str(x) for x in input_list]
    out_str = ",".join(str_list)
    return out_str


def str_or_type_format_func(input: Union[str, dict]) -> str:
    """Selects between _target_ (dict) and origignal str"""
    if isinstance(input, dict):
        if "_target_" not in input:
            raise KeyError(f"Key _target_ not in input: {input}")
        info: str = input["_target_"]
        info = rsplit_format_func(info)
    elif isinstance(input, str):
        info = input
    else:
        info = str(input)
    return info


def hydra_instance_format(input_data: Union[str, dict]) -> str:
    """Selects between _target_ (dict) and origignal str"""
    if isinstance(input_data, dict):
        if "_target_" not in input_data:
            raise KeyError(f"Key _target_ not in input: {input_data}")
        info: str = input_data["_target_"]
        info = rsplit_format_func(info) + "("
        args = [
            f"{cur_arg}={input_data[cur_arg]}"
            for cur_arg in input_data
            if cur_arg != "_target_"
        ]
        info += ",".join(args) + ")"

    elif isinstance(input_data, str):
        info = input_data
    else:
        info = str(input_data)
    return info


def rsplit_format_func(input_str: str) -> str:
    """Returns the last part after the dot"""
    if "." not in input_str:
        return input_str
    if input_str.endswith("."):
        input_str = input_str[:-1]
    return input_str.rsplit(".", maxsplit=1)[1]


def list_type_format_func(input_list: List[dict]):
    """Select from every list entry the _target_ component"""
    out_list = []
    for cur_type in input_list:
        out_list.append(str_or_type_format_func(cur_type))
    return out_list
