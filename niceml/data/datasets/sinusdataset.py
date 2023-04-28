from typing import List

from tensorflow.keras.utils import Sequence

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datainfos.datainfo import DataInfo
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext


class SinusDataset(Dataset, Sequence):
    def initialize(
        self, data_description: DataDescription, exp_context: ExperimentContext
    ):
        pass

    def __init__(
        self,
        batch_size: int,
        data_count: int,
        max_x: float,
        min_x: float,
        set_name: str,
    ):
        self.batch_size = batch_size
        self.data_count = data_count
        self.max_x = max_x
        self.min_x = min_x
        self.set_name = set_name

    def get_batch_size(self) -> int:
        return self.batch_size

    def get_set_name(self) -> str:
        return self.set_name

    def __getitem__(self, index: int):
        pass

    def get_datainfo(self, batch_index: int) -> List[DataInfo]:
        pass

    def __len__(self):
        pass

    def get_data_by_key(self, data_key):
        pass
