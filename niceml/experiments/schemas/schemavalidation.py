"""Module for the validating schemas"""
from typing import List

from niceml.experiments.experimentdata import ExperimentData
from niceml.experiments.schemas.expmember import ExpMember


def get_expmembers_from_class(cls) -> List[ExpMember]:
    """Returns all ExpMember from a given class"""
    exp_member_list: List[ExpMember] = [
        getattr(cls, member_name)
        for member_name in dir(cls)
        if isinstance(getattr(cls, member_name), ExpMember)
    ]
    return exp_member_list


def validate_schema(exp_data: ExperimentData, schema) -> bool:
    """validates the instance with the given schema"""
    exp_member_list: List[ExpMember] = get_expmembers_from_class(schema)
    is_valid_list = [x.validate(exp_data) for x in exp_member_list]
    return all(is_valid_list)
