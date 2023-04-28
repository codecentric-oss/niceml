"""Module with default data shuffler"""

from random import shuffle
from typing import List, Optional

from niceml.data.datainfos.datainfo import DataInfo
from niceml.data.datashuffler.datashuffler import DataShuffler


class DefaultDataShuffler(DataShuffler):
    """Default data shuffler to shuffle the indices of the data"""

    def shuffle(
        self, data_infos: List[DataInfo], batch_size: Optional[int] = None
    ) -> List[int]:
        indexes = list(range(len(data_infos)))
        shuffle(indexes)
        return indexes
