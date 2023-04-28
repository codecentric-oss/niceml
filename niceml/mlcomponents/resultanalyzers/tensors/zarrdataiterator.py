from collections import defaultdict
from typing import Dict, Optional, Tuple, Union

import numpy as np
import zarr

from niceml.mlcomponents.resultanalyzers.tensors.tensordataiterators import (
    TensordataIterator,
)


class ZarrDataIterator(TensordataIterator):
    """
    This iterator allows to iterate over a zarr data file.

    Parameters
    ----------
    scale_int_to_float: bool, default False
        Divides all values by 255
    use_key_splits: Optional[str], default None
        if not none it uses this to combine multiple files to one key.
    """

    def __init__(
        self, scale_int_to_float: bool = False, use_key_splits: Optional[str] = None
    ):
        self.scale_int_to_float = scale_int_to_float
        self.data = None
        self.data_info: Optional[dict] = None
        self.use_key_splits: Optional[str] = use_key_splits

    def _split_data_and_id(self, data_key: str) -> Tuple[str, str]:
        """splits the data depending on the use_key_splits"""
        if self.use_key_splits is None:
            return data_key, "default"
        splits = data_key.rsplit(self.use_key_splits, maxsplit=1)
        return splits[0], splits[1]

    def _get_data_id(self, data_key: str) -> str:
        return self._split_data_and_id(data_key)[0]

    def _get_data_type(self, data_key: str) -> str:
        return self._split_data_and_id(data_key)[1]

    def open(self, path: str):
        self.data = zarr.open(path + ".zarr", mode="r")
        self.data_info = defaultdict(dict)
        for cur_data_key in self.data:
            data_id = self._get_data_id(cur_data_key)
            self.data_info[data_id][self._get_data_type(cur_data_key)] = cur_data_key

    def __iter__(self):
        return iter(self.data_info)

    def __getitem__(self, item: str) -> Union[np.ndarray, Dict[str, np.ndarray]]:
        cur_data_info: dict = self.data_info[item]
        np_data_dict = {x: self.data[y][...] for x, y in cur_data_info.items()}
        if self.scale_int_to_float:
            np_data_dict = {x: y.astype(float) / 255.0 for x, y in np_data_dict.items()}

        if self.use_key_splits is None:
            return np_data_dict["default"]

        return np_data_dict
