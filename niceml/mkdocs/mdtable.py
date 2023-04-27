"""Module for markdowntable"""
from typing import List


def get_md_table(
    headings: List[str], col_widths: List[int], contents: List[List[str]]
) -> str:
    """Creates a markdown table as str"""
    table_str = get_table_line(col_widths, headings)
    table_str += get_char_line(col_widths)
    for cur_content in contents:
        table_str += get_table_line(col_widths, cur_content)
    return table_str


def get_table_line(col_widths: List[int], contents: List[str]) -> str:
    """Creates one line in an mdtable"""
    line: str = "|"
    for index, cur_col_width in enumerate(col_widths):
        cur_content: str = ""
        if len(contents) > index:
            cur_content = contents[index]
        line += (
            " "
            + cur_content[:cur_col_width]
            + " " * max(0, cur_col_width - len(cur_content))
            + " |"
        )
    return line + "\n"


def get_char_line(col_widths: List[int], used_char: str = "-"):
    """Returns one row line with the same char (used_char)"""
    assert len(used_char) == 1
    line: str = "|"
    for cur_col_width in col_widths:
        line += used_char * (cur_col_width + 2) + "|"
    return line + "\n"
