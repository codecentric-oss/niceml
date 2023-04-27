"""Module for regular expression utilities """
import re

# Pattern of experiment
EXP_NAME_PATTERN = r"[A-Za-z]+-\d{4}-(0?[1-9]|[1][0-2])-[0-9]+T(0?[0-9]|1[0-9]|2[0-3])\.[0-9]+\.(0?[0-9]|[1-5][0-9])\.\d{3}Z-id_[A-Za-z0-9]{4}"  # pylint: disable = line-too-long


def check_exp_name(exp_name: str) -> bool:
    """
    Checks if an experiment name matches a pattern (EXP_NAME_PATTERN)
    Args:
        exp_name: experiment name to check

    Returns:
        True if `exp_name` matches the pattern
    """
    pattern = re.compile(EXP_NAME_PATTERN)
    return bool(pattern.match(exp_name))
