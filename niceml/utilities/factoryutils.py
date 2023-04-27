"""Modul for factory utilities"""
from dataclasses import asdict, dataclass, is_dataclass
from importlib import import_module
from pathlib import Path
from typing import Any, Optional, Union

from niceml.config.envconfig import replace_id_keys


class NoValidParameterPathError(Exception):
    """Exception if parameter path is not valid"""

    pass


class ImportExceptionError(Exception):
    """Exception if an import is not possible"""

    pass


class InitializationParamsError(Exception):
    """Exception for invalid initialization parameters"""

    pass


def init_object(
    input_dict: Union[dict, list],
    additional_info: Optional[Union[dict, dataclass]] = None,
) -> Any:
    """
    Imports a class or function dynamically.
    When `type` is used the object is initialized with the given `params` accordingly.
    Otherwise (with `function`-keyword), only the imported object is returned.

    Args:
        input_dict: Dict with keywords (type and params) or function.
    additional_info: Additional information about to use for initialization.

    Returns:
        Initialized or imported object/class/function.
    """
    if is_dataclass(additional_info):
        additional_info = asdict(additional_info)

    if additional_info is None:
        additional_info = {}

    if isinstance(input_dict, list):
        return [init_object(x, additional_info) for x in input_dict]

    use_params: bool = False
    if "type" in input_dict:
        cur_type: str = input_dict["type"]
        use_params = True
    elif "function" in input_dict:
        cur_type: str = input_dict["function"]
    else:
        raise ImportExceptionError("Neither type nor function keyword in param dict!")

    type_list = cur_type.rsplit(".", 1)
    try:
        imported_module = import_module(type_list[0])
    except ModuleNotFoundError as error:
        raise Exception(f"Module with name not found: {type_list[0]}") from error
    imported_type = getattr(imported_module, type_list[1])
    if use_params:
        init_dict = input_dict.get("params", {})
        try:
            init_class = imported_type(**init_dict, **additional_info)
        except TypeError as error:
            raise InitializationParamsError(
                f"Failed to initialize: {cur_type}"
            ) from error
    else:
        init_class = imported_type

    return init_class


def import_function(function_name: str):
    """
    Takes a string as input and returns the function object that is referenced by the string.
    The string must be in the format of 'module_name.class_name'. The import_module function
    from Python's built-in importlib module is used to import the module, and then getattr()
    is used to retrieve an attribute from it (the class).

    Args:
        function_name: str: Specify the type of the parameter
    Returns:
         Function object
    """
    type_list = function_name.rsplit(".", 1)
    try:
        imported_module = import_module(type_list[0])
    except ModuleNotFoundError as e:
        raise Exception(f"Module with name not found: {type_list[0]}") from e
    return getattr(imported_module, type_list[1])


def subs_path_and_create_folder(filepath: str, short_id: str, run_id: str) -> str:
    """
    Takes a filepath, and replaces the keys 'short_id' and 'run_id' with the corresponding
    values. It then creates any necessary folders in order to make the path valid.

    Args:
        filepath: Pass the filepath to the function
        short_id: Replace the short_id key in the filepath string
        run_id: Create a unique folder for each run
    Returns:
         filepath with replaced short id and run id
    """
    filepath = replace_id_keys(filepath, short_id, run_id)
    filepath_obj = Path(filepath)
    filepath_obj.parent.mkdir(parents=True, exist_ok=True)
    return filepath
