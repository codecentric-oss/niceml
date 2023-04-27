"""Module of the HealthDataset"""
from os.path import join

from tensorflow.keras.utils import (  # pylint: disable=import-error,no-name-in-module
    Sequence,
)

from niceml.data.dataloaders.dfloaders import SimpleDfLoader
from niceml.data.datasets.dfdataset import DfDataset


# QUEST: Remove? If yes, remove DfDataset as well?


class HealthDataset(DfDataset, Sequence):
    """Specific Healthdata generator for sample data"""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        id_key: str,
        batch_size: int,
        set_name: str,
        filename: str,
        filepath: str,
        shuffle: bool = False,
    ):
        df_loader = SimpleDfLoader()
        df_path = join(filepath, filename)
        super().__init__(id_key, batch_size, set_name, df_loader, df_path, shuffle)

    def get_dataset_stats(self) -> dict:
        gender_count = self.dataframe["sex"].value_counts().to_dict()
        smoker_count = self.dataframe["smoker"].value_counts().to_dict()
        return dict(size=len(self.index_list), **gender_count, smoker=smoker_count)
