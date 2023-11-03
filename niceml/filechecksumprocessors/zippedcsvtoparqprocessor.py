"""Module for implementation of ZippedCsvToParqProcessor"""

import zipfile
from collections import defaultdict
from os.path import basename, splitext
from typing import Dict, List, Tuple, Optional, Union

import pandas as pd
from tqdm import tqdm

from niceml.filechecksumprocessors.filechecksumprocessor import FileChecksumProcessor
from niceml.utilities.checksums import md5_from_file
from niceml.utilities.fsspec.locationutils import (
    open_location,
    LocationConfig,
    join_fs_path,
    join_location_w_path,
)
from niceml.utilities.ioutils import list_dir, write_parquet
from niceml.utilities.splitutils import clear_folder


class ZippedCsvToParqProcessor(FileChecksumProcessor):
    """Implementation of a FileChecksumProcessor to convert zip archives
    with csv files into parquet files"""

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
        csv_seperator: str = ";",
        clear: bool = False,
        recursive: bool = False,
    ):
        """
        FileChecksumProcessor that can be used as part of a pipeline to
        process files based on the checksum.
        Args:
            input_location: Input location of the Processor
            output_location: Output location of the Processor
            lockfile_location: Location of the checksum lockfile
            debug: Flag to activate the debug mode
            process_count: Amount of processes for parallel execution
            batch_size: Size of a batch
            csv_seperator: Seperator character for the csv files.
            clear: Flag to clear the output location when initialize the Processor
            recursive: Flag indicating whether the input location should be
                        searched for files recursively
        """
        super().__init__(
            input_location=input_location,
            output_location=output_location,
            lockfile_location=lockfile_location,
            debug=debug,
            process_count=process_count,
            batch_size=batch_size,
            lock_file_name=lock_file_name,
        )
        self.recursive = recursive
        self.clear = clear
        self.csv_seperator = csv_seperator

        if self.clear:
            clear_folder(self.output_location)

    def list_files(self) -> Tuple[List[str], List[str]]:
        """
        Returns a tuple of two lists:
            1. A list of all files in the input location
            2. A list of all files in the output location

        Returns:
            A tuple of two lists
        """
        with open_location(self.input_location) as (input_fs, input_path):
            input_files = list_dir(
                path=input_path,
                recursive=self.recursive,
                file_system=input_fs,
                filter_ext=[".zip"],
            )
            input_files = [
                join_fs_path(input_fs, input_path, input_file)
                for input_file in input_files
            ]
        with open_location(self.output_location) as (output_fs, output_path):
            output_fs.makedirs(output_path, exist_ok=True)
            output_files = list_dir(
                path=output_path,
                recursive=self.recursive,
                file_system=output_fs,
                filter_ext=[".parq"],
            )
            output_files = [
                join_fs_path(output_fs, output_path, output_file)
                for output_file in output_files
            ]

        return input_files, output_files

    def generate_batches(
        self,
        input_file_list: List[str],
        changed_files_dict: Dict[str, Dict[str, bool]],
        output_file_list: Optional[List[str]] = None,
        force: bool = False,
    ) -> List[Dict[str, List[str]]]:
        """
        The generate_batches function is responsible for generating a list of batches,
        where each batch is a dictionary with `inputs` as a key, followed by a list of file paths

        Args:
            input_file_list: List[str]: A list of input file names
            changed_files_dict: Dict[str: Dict[str:bool]]: Dictionary with the information
            which files have changed
            output_file_list: List[str]: A optional list of output file names
            force: bool: Force the generation of batches even if no files have changed

        Returns:
            A list of batches, each batch is a dictionary with one key `inputs`
            and the value is a list of file paths
        """
        if not force:
            input_file_list = [
                file_name
                for file_name, changed in changed_files_dict["inputs"].items()
                if changed
            ]
        batches = []
        for batch_pos in range(0, len(input_file_list), self.batch_size):
            batches.append(
                {"inputs": input_file_list[batch_pos : batch_pos + self.batch_size]}
            )
        return batches

    def process(self, batch: Dict[str, List[str]]) -> Dict[str, Dict[str, str]]:
        """
        The process function takes a batch of files and converts them from CSV to Parquet.

        Args:
            self: Access the class attributes
            batch: Dict[str: Pass in the batch of files to be processed
            List[str]]: Pass in the list of files that are to be processed

        Returns:
            A dictionary of checksums for each file in `self.output_location`
            (key = `outputs`) and `self.input_location` (key = `inputs`)
        """
        checksums = defaultdict(dict)

        with open_location(self.input_location) as (input_file_system, input_root):
            for zip_file in tqdm(
                batch["inputs"], desc="Extract zip files of current batch"
            ):
                with input_file_system.open(zip_file) as opened_zip_file:
                    checksums["inputs"][zip_file] = md5_from_file(
                        file_path=zip_file, file_system=input_file_system
                    )

                    zf = zipfile.ZipFile(opened_zip_file)
                    csv_files = zf.namelist()
                    for csv_file in csv_files:
                        with zf.open(csv_file, mode="r") as opened_csv_file:
                            df = pd.read_csv(
                                opened_csv_file,
                                sep=self.csv_seperator,
                                low_memory=False,
                            )
                        parq_name = basename(splitext(csv_file)[0]) + ".parq"
                        output_df_location = join_location_w_path(
                            self.output_location, parq_name
                        )
                        with open_location(output_df_location) as (
                            output_file_system,
                            output_df_path,
                        ):
                            write_parquet(
                                df, output_df_path, file_system=output_file_system
                            )
                            checksums["outputs"][output_df_path] = md5_from_file(
                                file_path=output_df_path, file_system=output_file_system
                            )
        return checksums
