"""Module for utils which are used for split data"""

from dataclasses import dataclass
from os.path import basename, join, splitext
from typing import List, Tuple, Union

import numpy as np

from niceml.utilities.checksums import md5_from_file
from niceml.utilities.copyutils import CopyFileInfo
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_location_w_path,
    open_location,
)
from niceml.utilities.idutils import ALPHANUMERICLIST
from niceml.utilities.ioutils import list_dir


@dataclass
class DataSetInfo:
    """Dataclass which represents a data set info including
    a set name (e.g. test) and a probability to split the dataset"""

    set_name: str
    probability: float

    def to_tuple(self) -> Tuple[str, float]:
        """Returns a tuple with shape (set_name,probability)"""
        return self.set_name, self.probability


def init_dataset_info(info: str) -> DataSetInfo:
    """
    Returns a DataSetInfo for the given information

    Args:
        info: string with the format [set_name,probability], e.g. 'test,0.1'

    Returns:
        DataSetInfo object with set and probability information
    """
    set_name, prob = info.split(",")
    prob = float(prob)
    return DataSetInfo(set_name=set_name, probability=prob)


def generate_set_and_prob_list(
    set_info_list: List[DataSetInfo],
) -> Tuple[List[str], List[float]]:
    """
    Takes a list of DataSetInfo objects and returns two lists:
        1. List of Names of each set in the order they appear in the input list.
        2. Corresponding list containing each set's probability, also in order.

    Args:
        set_info_list: List of DataSetInfo objects
    Returns:
        A list of names (str) and a list of probabilities (float)
    """
    tmp_list: List[Tuple[str, float]] = [dsf.to_tuple() for dsf in set_info_list]
    names, probs = zip(*tmp_list)
    return list(names), list(probs)


# pylint:disable= too-many-arguments,too-many-locals
def create_copy_files_container(
    folder_list: List[str],
    input_location: Union[dict, LocationConfig],
    recursive: bool,
    dataset_info_list: List[DataSetInfo],
    delimiter_maxsplit: int,
    name_delimiter: str,
    output_location: Union[dict, LocationConfig],
) -> List[CopyFileInfo]:
    """
    Creates a list of CopyFileInfo objects.
    The CopyFileInfo object contains the input and output locations for
    each file, as well as the checksum of that file.
    This function also takes in a list of DataSetInfo objects, which contain
    information about how many files should be copied into each set (train/validation/test).
    It then uses this information to randomly assign files into sets based on their probability.

    Args:
        folder_list: Folders to copy from
        input_location: Location of the input data (path) with corresponding LocationConfig
        recursive: Indicate whether to recursively search for files in the input_location
        dataset_info_list: Determine the name and probability of each dataset
        delimiter_maxsplit: Maxsplit to split the file name into a set and an identifier
        name_delimiter:  Delimiter to split the file name into a set and an identifier
        output_location: Location of the output files (path) with corresponding LocationConfig
    Returns:
         A list of CopyFileInfo objects with input and output location and the files checksum
    """
    set_list, prob_list = generate_set_and_prob_list(dataset_info_list)
    copy_list: List[CopyFileInfo] = []
    with open_location(input_location) as (input_fs, input_path):
        for input_folder in folder_list:
            files: List[str] = [
                x
                for x in list_dir(
                    join(input_path, input_folder),
                    recursive=recursive,
                    file_system=input_fs,
                )
                if input_fs.isfile(join(input_path, input_folder, x))
            ]
            for file in files:
                cur_basename = basename(splitext(file)[0])
                if delimiter_maxsplit > 0 and name_delimiter in cur_basename:
                    cur_basename = cur_basename.rsplit(
                        name_delimiter, maxsplit=delimiter_maxsplit
                    )[0]
                identifier = "".join(
                    [char for char in cur_basename if char in ALPHANUMERICLIST]
                )
                cur_seed = int(identifier, base=len(ALPHANUMERICLIST)) % (2 ** 32 - 1)
                rng = np.random.default_rng(seed=cur_seed)
                drawn_set = rng.choice(set_list, 1, p=prob_list)[0]
                output_file = join(drawn_set, file)
                input_file_path = join(input_folder, file)
                checksum = md5_from_file(
                    join(input_path, input_file_path), file_system=input_fs
                )
                file_input_location = join_location_w_path(
                    input_location, input_file_path
                )
                file_output_location = join_location_w_path(
                    output_location, output_file
                )
                copy_list.append(
                    CopyFileInfo(file_input_location, file_output_location, checksum)
                )
    return copy_list


# pylint:disable=broad-except
def clear_folder(location: Union[dict, LocationConfig]):
    """Deletes every file or folder inside a given location"""
    with open_location(location) as (target_fs, path):
        if target_fs.exists(path):
            try:
                target_fs.rm(path, recursive=True)
            except Exception as error:
                print(f"Failed to delete {path}. Reason: {error}")
