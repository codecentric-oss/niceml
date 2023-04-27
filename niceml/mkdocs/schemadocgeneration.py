"""Module for generating markdown docs for schemas"""
from typing import List

from niceml.experiments.schemas.expmember import ExpMember, FolderMember
from niceml.experiments.schemas.schemalist import get_all_schemas
from niceml.experiments.schemas.schemavalidation import get_expmembers_from_class
from niceml.mkdocs.mdtable import get_md_table


def get_all_expschema_markdowns(col_widths: List[int]) -> str:
    """Returns all schemas as md str"""
    mk_str = ""
    for exp_schema in get_all_schemas():
        mk_str += expschema_to_markdown(exp_schema, col_widths) + "\n\n"

    return mk_str


def expschema_to_markdown(exp_schema_cls, col_widths: List[int]) -> str:
    """Converts an expschema to a markdown table"""
    cur_md: str = f"## `{exp_schema_cls.__name__}`\n\n"
    cur_md += exp_schema_cls.__doc__ + "\n\n" or ""
    exp_member_list: List[ExpMember] = get_expmembers_from_class(exp_schema_cls)
    headings: List[str] = ["File", "Description"]
    contents: List[List[str]] = []
    for member in sorted(exp_member_list):
        icon = get_icon(member)
        contents.append([f"{icon} `{member.path}`", member.description])
    cur_md += get_md_table(headings, col_widths, contents)
    return cur_md


def get_icon(member: ExpMember) -> str:
    """Returns an icon according the member type"""
    if isinstance(member, FolderMember):
        return ":file_folder:"
    return ":material-file:"
