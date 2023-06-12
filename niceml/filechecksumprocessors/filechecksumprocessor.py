from abc import ABC, abstractmethod
from typing import Tuple, List, Any, Dict, Union

from niceml.utilities.fsspec.locationutils import LocationConfig, open_location
from niceml.utilities.ioutils import read_yaml


class FileChecksumProcessor(ABC):

    def __init__(self, input_location: Union[dict, LocationConfig], output_location: Union[dict, LocationConfig], lockfile_location: Union[dict, LocationConfig],
                 debug: bool = False, process_count: int = 8):
        self.input_location = input_location
        self.output_location = output_location
        self.lockfile_location = lockfile_location
        self.debug = debug
        self.process_count = process_count

    def load_checksums(self) -> Dict[str, Dict[str, str]]:
        """Loads checksums from lockfile"""
        with open_location(self.lockfile_location) as (lockfile_fs, lockfile_path):
            checksum_dict = read_yaml(lockfile_path, file_system=lockfile_fs)
        return checksum_dict

    @abstractmethod
    def list_files(self) -> Tuple[List[str], List[str]]:
        """Lists input and output files and
        returns them as lists of strings"""

    @abstractmethod
    def generate_batches(self, input_file_list: List[str], output_file_list: List[str], changed_files_dict: Dict[str, Dict[str, bool]]) -> List[Any]:
        """Generates batches of input and output files
        and returns them as a list"""

    def remove_not_required_outputs(self, output_file_list: List[str]) -> None:
        """Removes output files that are not required anymore"""
        pass

    def find_changed_files(self, input_file_list: List[str], output_file_list: List[str], checksum_dict: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, bool]]:
        """Filters input and output files that are not required to be reprocessed"""
        input_files_changed = check_files_changed(self.input_location, input_file_list, checksum_dict["inputs"])
        output_files_changed = check_files_changed(self.output_location, output_file_list, checksum_dict["outputs"])

        return dict(inputs=input_files_changed, outputs=output_files_changed)

    @abstractmethod
    def process_batch(self, batch: Any):
        """Processes a batch of files"""

    def process(self, force: bool = False) -> None:
        """Processes files"""
        checksum_dict = self.load_checksums()
        input_file_list, output_file_list = self.list_files()
        input_files_changed, output_files_changed = self.find_changed_files(input_file_list, output_file_list, checksum_dict)
        self.remove_not_required_outputs(output_file_list)
        batches = self.generate_batches(input_file_list, output_file_list)
        with Pool(self.threads) as pool:
            for idx, process_result in enumerate(
                    pool.imap_unordered(self._process, tqdm(input_lenses_to_process))
            ):
                if process_result is not None:
                    lens_data_info, output_file_list = process_result
                    cur_lock_dict: Dict[str, Optional[str]] = {
                        "inputs": hex_leading_zeros(lens_data_info.deep_hash()),
                        "outputs": get_file_list_hash(output_file_list),
                    }
                    self.lock_data[lens_data_info.lens_id] = cur_lock_dict
                if idx % 10 == 0:
                    with open_location(self.lockfile_location) as (
                            lockfile_fs,
                            lockfile_root,
                    ):
                        write_json(
                            self.lock_data, lockfile_root, file_system=lockfile_fs
                        )

def check_files_changed(location: Union[dict, LocationConfig], file_list: List[str], checksum_dict: Dict[str, str]) -> Dict[str, bool]:
    """Checks if files in a location have changed"""
    pass