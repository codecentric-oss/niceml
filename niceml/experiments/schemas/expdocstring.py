"""Module for the experiment_docstring"""
from typing import List

from niceml.experiments.schemas.expmember import ExpMember
from niceml.experiments.schemas.schemavalidation import get_expmembers_from_class


def experiment_docstring(cls):
    """extends the docstring of a experiment class with its attributes"""
    cur_doc: str = cls.__doc__ or ""
    cur_doc = f"{cls.__name__}\n{'#'*len(cls.__name__)}\n\n" + cur_doc + "\n\n"
    exp_member_list: List[ExpMember] = get_expmembers_from_class(cls)
    for member in sorted(exp_member_list):
        cur_doc += f"{member.get_docstring()}\n\n"
    cls.__doc__ = cur_doc
    return cls
