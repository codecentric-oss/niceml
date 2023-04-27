"""Module for utils for logging"""
from typing import List


def get_logstr_from_dict(log_dict: dict):
    """Combines a dict to a single str"""
    str_list: List[str] = [f"{key}: {value}" for key, value in log_dict.items()]
    ret_str: str = "\n".join(str_list)
    return ret_str
