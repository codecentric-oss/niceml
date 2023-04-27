"""Module for copying files"""
from dataclasses import dataclass
from os.path import basename, dirname
from typing import List, Union

from fsspec import AbstractFileSystem
from tqdm import tqdm

from niceml.utilities.checksums import md5_from_file
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_fs_path,
    open_location,
)


@dataclass
class CopyInfo:
    """This class contains the information for copying files between filesystems"""

    location: Union[LocationConfig, dict]
    copy_filelist: List[str]

    def copy_to_filesystem(
        self, target_filesystem: AbstractFileSystem, target_path: str
    ):
        """Copies the files to a target path in the target filesystem"""
        with open_location(self.location) as (source_file_system, root_path):
            for src_file in self.copy_filelist:
                tgt_file = join_fs_path(
                    target_filesystem, target_path, basename(src_file)
                )
                target_filesystem.makedirs(target_path, exist_ok=True)
                with source_file_system.open(
                    join_fs_path(source_file_system, root_path, src_file), "rb"
                ) as fsrc, target_filesystem.open(tgt_file, "wb") as ftgt:
                    ftgt.write(fsrc.read())


@dataclass
class CopyFileInfo:
    """Dataclass which is used to compare an input file with an output file"""

    input_location: Union[LocationConfig, dict]
    output_location: Union[LocationConfig, dict]
    checksum: str = ""

    def copy_file(self):
        """Copies the input file to the output location"""
        with open_location(self.input_location) as (input_filesystem, input_path):
            with open_location(self.output_location) as (
                output_filesystem,
                output_path,
            ):
                output_filesystem.makedirs(dirname(output_path), exist_ok=True)
                with input_filesystem.open(
                    input_path, "rb"
                ) as fsrc, output_filesystem.open(output_path, "wb") as ftgt:
                    ftgt.write(fsrc.read())


def process_copy_files(copy_file_list: List[CopyFileInfo]):
    """Copies/symlinks all files without any checks from input to output location"""
    file_info: CopyFileInfo
    for file_info in tqdm(copy_file_list):
        file_info.copy_file()


def filter_for_required(copy_file_list: List[CopyFileInfo]) -> List[CopyFileInfo]:
    """
    Checks if a copying files from input to output location is required.
    If a file already exists in the output location and has not changed (same filehash),
    copying this file is not required.
    Args:
        copy_file_list: list of files to check

    Returns:
        List of files that are required to be copy
    """
    file_info: CopyFileInfo
    to_copy_info_list: List[CopyFileInfo] = []
    for file_info in tqdm(copy_file_list):
        with open_location(file_info.output_location) as (
            output_filesystem,
            output_path,
        ):
            if not (
                output_filesystem.isfile(output_path)
                and md5_from_file(output_path, output_filesystem) == file_info.checksum
            ):
                to_copy_info_list.append(file_info)
    return to_copy_info_list
