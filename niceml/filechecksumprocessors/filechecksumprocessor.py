"""Module for abstract implementation of FileChecksumProcessor"""
from abc import ABC, abstractmethod
from collections import defaultdict
from multiprocessing.pool import Pool
from typing import Tuple, List, Any, Dict, Union, Optional

from pydantic.utils import deep_update
from tqdm import tqdm

from niceml.utilities.checksums import md5_from_file
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    open_location,
    join_fs_path,
)
from niceml.utilities.ioutils import read_yaml, list_dir, write_yaml


class FileChecksumProcessor(ABC):
    """FileChecksumProcessor that can be used as part of a pipeline to process
    files based on the checksum"""

    # ruff: noqa: PLR0913
    def __init__(
        self,
        input_location: Union[dict, LocationConfig],
        output_location: Union[dict, LocationConfig],
        lockfile_location: Union[dict, LocationConfig],
        lock_file_name: str = "lock.yaml",
        debug: bool = False,
        process_count: int = 8,
        batch_size: int = 16,
    ):
        """
        FileChecksumProcessor that can be used as part of a pipeline to process
        files based on the checksum.
        Args:
            input_location: Input location of the Processor
            output_location: Output location of the Processor
            lockfile_location: Location of the checksum lockfile
            debug: Flag to activate the debug mode
            process_count: Amount of processes for parallel execution
            batch_size: Size of a batch
        """
        self.lock_file_name = lock_file_name
        self.input_location = input_location
        self.output_location = output_location
        self.lockfile_location = lockfile_location
        self.debug = debug
        self.process_count = process_count
        self.lock_data: Dict[str, dict] = defaultdict(dict)
        self.batch_size = batch_size

    def load_checksums(self) -> Dict[str, Dict[str, str]]:
        """Loads checksums from lockfile"""
        with open_location(self.lockfile_location) as (lockfile_fs, lockfile_path):
            try:
                checksum_dict = read_yaml(
                    join_fs_path(lockfile_fs, lockfile_path, self.lock_file_name),
                    file_system=lockfile_fs,
                )
            except FileNotFoundError:
                checksum_dict = defaultdict(dict)
        return checksum_dict

    @abstractmethod
    def list_files(self) -> Tuple[List[str], List[str]]:
        """Lists input and output files and
        returns them as lists of strings"""

    @abstractmethod
    def generate_batches(
        self,
        input_file_list: List[str],
        changed_files_dict: Dict[str, Dict[str, bool]],
        output_file_list: Optional[List[str]] = None,
        force: bool = False,
    ) -> List[Any]:
        """Generates batches of input and output files
        and returns them as a list"""

    def remove_not_required_outputs(self, output_file_list: List[str]) -> None:
        """Removes output files that are not required anymore"""
        with open_location(self.output_location) as (output_fs, output_root):
            files_in_output_location = list_dir(path=output_root, file_system=output_fs)
            files_in_output_location = [
                join_fs_path(output_fs, output_root, output_file)
                for output_file in files_in_output_location
            ]
            file_diff = list(set(files_in_output_location) - set(output_file_list))
            for file in file_diff:
                output_fs.rm_file(join_fs_path(output_fs, output_root, file))

    def find_changed_files(
        self,
        input_file_list: List[str],
        output_file_list: List[str],
        checksum_dict: Dict[str, Dict[str, str]],
    ) -> Dict[str, Dict[str, bool]]:
        """Filters input and output files that are not required to be reprocessed"""
        input_files_changed = check_files_changed(
            self.input_location,
            input_file_list,
            checksum_dict["inputs"] if "inputs" in checksum_dict else None,
        )
        output_files_changed = check_files_changed(
            self.output_location,
            output_file_list,
            checksum_dict["outputs"] if "outputs" in checksum_dict else None,
        )

        return dict(inputs=input_files_changed, outputs=output_files_changed)

    @abstractmethod
    def process(self, batch: Any) -> Dict[str, Any]:
        """
        Processes a batch of files.
        Returns a dict of input and output files with the updated checksums
        e.g. {"inputs":{"filename":"checksum"}, "outputs":{"filename":"checksum"}}
        """

    def run_process(self, force: bool = False) -> None:
        """Processes files"""
        checksum_dict = self.load_checksums()
        input_file_list, output_file_list = self.list_files()

        self.remove_not_required_outputs(output_file_list)
        checksum_dict = remove_deleted_checksums(
            input_file_list=input_file_list,
            output_file_list=output_file_list,
            checksum_dict=checksum_dict,
        )

        changed_files_dict = (
            self.find_changed_files(  # TODO right place or better in line 82
                input_file_list, output_file_list, checksum_dict
            )
        )

        processing_list = self.generate_batches(
            input_file_list, changed_files_dict, force=force
        )

        def _process_result(result, index: int):
            if result is not None:
                self.lock_data = deep_update(self.lock_data, result)
            if (index % 10 == 0) or (len(processing_list) == (index + 1)):
                with open_location(self.lockfile_location) as (
                    lockfile_fs,
                    lockfile_root,
                ):
                    write_yaml(
                        dict(self.lock_data),
                        join_fs_path(lockfile_fs, lockfile_root, self.lock_file_name),
                        file_system=lockfile_fs,
                    )

        if self.debug:
            for idx, batch in enumerate(processing_list):
                process_result = self.process(batch)
                _process_result(process_result, idx)
        else:
            with Pool(self.process_count) as pool:
                for idx, process_result in enumerate(
                    tqdm(
                        pool.imap_unordered(self.process, processing_list),
                        total=len(processing_list),
                        desc="Process batches",
                    )
                ):
                    _process_result(process_result, idx)


def remove_deleted_checksums(
    input_file_list: List[str],
    output_file_list: List[str],
    checksum_dict: Dict[str, Dict[str, str]],
) -> Dict[str, Dict[str, str]]:
    """
    Takes in a list of input files, a list of output files, and
    a dictionary containing the checksums for all the files. It returns an updated version of that
    dictionary with only those keys corresponding to either input or output file names.

    Args:
        input_file_list: List[str]: Specify the input files
        output_file_list: List[str]: Specify the output files
        checksum_dict: Dict[str,Dict[str,str]]: Dictionary with the checksums
                        of the input and output files

    Returns:
        A dictionary of dictionaries with the updated checksums of the input and output files
    """
    existing_checksums = defaultdict(dict)
    existing_checksums["inputs"] = {
        key: value
        for key, value in checksum_dict["inputs"].items()
        if key in input_file_list
    }
    existing_checksums["outputs"] = {
        key: value
        for key, value in checksum_dict["outputs"].items()
        if key in output_file_list
    }
    return existing_checksums


def check_files_changed(
    location: Union[dict, LocationConfig],
    file_list: List[str],
    checksum_dict: Optional[Dict[str, str]] = None,
) -> Dict[str, bool]:
    """Checks if files in a location have changed"""
    changed_checksums_dict = {}
    with open_location(location) as (location_fs, location_root):
        for file_path in file_list:
            if checksum_dict is not None:
                if file_path in checksum_dict.keys():
                    if (
                        md5_from_file(file_path=file_path, file_system=location_fs)
                        == checksum_dict[file_path]
                    ):
                        changed_checksums_dict[file_path] = False
                        continue

            changed_checksums_dict[file_path] = True

    return changed_checksums_dict
