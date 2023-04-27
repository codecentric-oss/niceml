"""Module for calculating checksums"""
import hashlib
import os
from os.path import isdir
from typing import Optional, Union

import click
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem

from niceml.utilities.ioutils import list_dir


def md5_from_file(
    file_path: str, file_system: Optional[AbstractFileSystem] = None
) -> str:
    """
    Calculates the md5 hash of a file
    Args:
        file_path: path to file to hash
        file_system: filesystem where the file is stored

    Returns:
        hash of file
    """
    cur_fs = file_system or LocalFileSystem()
    with cur_fs.open(file_path, "rb") as file:
        data = file.read()
    return hashlib.md5(data).hexdigest()


def md5_from_filelist_or_dir(
    file_list: Union[list, str], file_system: Optional[AbstractFileSystem] = None
) -> str:
    """
    Calculates the md5 hash of a list of files or a directory

    Args:
        file_list: List of files to hash or directory of files to hash
        file_system: Filesystem where the files are stored; Default = local

    Returns:
        A hash of one or more files
    """
    cur_fs = file_system or LocalFileSystem()
    if isinstance(file_list, list):
        md5_hash = hex_leading_zeros(0)
        for file in file_list:
            if isdir(file):
                cur_hash = md5_from_filelist_or_dir(
                    [
                        os.path.join(file, f)
                        for f in sorted(list_dir(file, return_full_path=True))
                    ],
                    file_system=cur_fs,
                )
            else:
                cur_hash = md5_from_filelist_or_dir(file, file_system=cur_fs)
            md5_hash = combine_checksums(cur_hash, md5_hash)
        return md5_hash
    if isinstance(file_list, str):
        return md5_from_file(file_list, file_system=cur_fs)

    raise Exception(f"Unknown type: {type(file_list)}")


def combine_checksums(first_hash, second_hash) -> str:
    """Combines two checksums"""
    if first_hash is None:
        return second_hash
    if second_hash is None:
        return first_hash
    value = int(first_hash, 16) ^ int(second_hash, 16)
    return hex_leading_zeros(value)


def hex_leading_zeros(value, length=32) -> str:
    """Returns a hex string with leading zeros of given length"""
    return f"{value:#0{length}x}"


@click.command()
@click.argument("output_file")
@click.argument("file_list", nargs=-1)
@click.option("--fileservice", default=None)
def gen_hash_command(output_file, file_list):
    """Command line interface for file hash calculation"""
    file_list = list(file_list) if isinstance(file_list, tuple) else [file_list]
    gen_hash_main(output_file, file_list)


def gen_hash_main(output_file, file_list):
    """Main function for file hash calculation"""
    md5_hash = md5_from_filelist_or_dir(file_list)
    with open(output_file, "w") as file:  # pylint: disable=unspecified-encoding
        file.write(md5_hash)


if __name__ == "__main__":
    gen_hash_command()  # pylint: disable=no-value-for-parameter
