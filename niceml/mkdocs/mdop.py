"""Module for generating markdown strings for dagster ops"""
from typing import Dict, List

from dagster._core.definitions import NodeDefinition

from niceml.mkdocs.mdtable import get_md_table
from dagster import Field


def get_md_op(op_def: NodeDefinition) -> str:
    """generates markdown strings for dagster ops"""
    col_widths: List[int] = [80, 120]
    op_fields = get_op_fields(op_def)
    headings: List[str] = ["ConfigKey", "Description"]
    cur_md: str = f"### Op: `{op_def.name}`\n\n"
    if op_def.description is not None:
        cur_md += op_def.description + "\n\n"
    contents: List[List[str]] = []
    for config_key in sorted(op_fields):
        desc = op_fields[config_key].description or ""
        contents.append([f"`{config_key}`", desc.replace("\n", " ")])
    cur_md += get_md_table(headings, col_widths, contents)
    cur_md += "\n\n"
    return cur_md


def get_op_fields(op_def: NodeDefinition) -> Dict[str, Field]:
    """returns fields from OpDefinition"""
    try:
        return op_def.config_schema.config_type.fields
    except AttributeError:
        return dict()
