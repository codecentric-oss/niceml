from abc import ABC, abstractmethod
from typing import Any, List, Optional

import numpy as np

from niceml.data.datadescriptions.datadescription import DataDescription


class NetInputTransformer(ABC):
    def __init__(self, data_description: Optional[DataDescription] = None):
        self.data_description = data_description

    def initialize(self, data_description: DataDescription):
        self.data_description: DataDescription = data_description

    @abstractmethod
    def get_net_inputs(self, data_list: List[Any]) -> np.ndarray:
        pass


class NetTargetTransformer(ABC):
    def __init__(self, data_description: Optional[DataDescription] = None):
        self.data_description = data_description

    def initialize(self, data_description: DataDescription):
        self.data_description: DataDescription = data_description

    @abstractmethod
    def get_net_targets(self, data_list: List[Any]) -> np.ndarray:
        pass
