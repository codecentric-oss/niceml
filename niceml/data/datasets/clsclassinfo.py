import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Union

import numpy as np

from niceml.data.datainfos.clsdatainfo import ClsDataInfo
from niceml.utilities.commonutils import items_from_shuffled_list


# QUEST: Right package?


class DuplicateClassNameError(Exception):
    pass


@dataclass
class ClsClassInfo:
    """
    This class can represent one classification class.

    Parameters:
    -----------
    name: str
        name of the class, usually the same as the folder name
    weight: float, default 1.0
        of this class are taken `weight * count` samples (e.g. for training)
    subclasses: List[str], default []
         integrates the listed classes to this class. They are represented by
         the actual `name` field of this object.
    """

    name: str
    weight: float = 1.0
    subclasses: list = field(default_factory=list)

    def __contains__(self, item: str):
        return item == self.name or item in self.subclasses


class ClsClassInfoList:
    def __init__(self, cls_info_list: List[ClsClassInfo]):
        self.cls_info_list = cls_info_list
        self.class_set = set()
        class_info: ClsClassInfo
        for class_info in self.cls_info_list:
            if class_info.name in self.class_set:
                raise DuplicateClassNameError(
                    f"Name {class_info.name} is used more than once!"
                )
            self.class_set.add(class_info.name)
            for subclass in class_info.subclasses:
                if subclass in self.class_set:
                    raise DuplicateClassNameError(
                        f"Subclass {subclass} of "
                        f"{class_info.name} is used more than once!"
                    )
                self.class_set.add(subclass)

    def __contains__(self, item: str):
        return item in self.class_set

    def __len__(self):
        return len(self.cls_info_list)

    def __iter__(self):
        return self.cls_info_list.__iter__()

    def __getitem__(self, item: int) -> ClsClassInfo:
        return self.cls_info_list[item]

    def index(self, item: str) -> int:
        for idx, class_info in enumerate(self.cls_info_list):
            if item in class_info:
                return idx
        raise ValueError(f"{item} is not in list")

    def get_class_name(self, folder_name: str) -> str:
        class_info: ClsClassInfo
        for class_info in self.cls_info_list:
            if folder_name in class_info:
                return class_info.name
        raise ValueError(f"{folder_name} not in class list")

    def has_custom_weighting(self) -> bool:
        return any((x.weight != 1.0 for x in self.cls_info_list))

    def get_class_weights(self) -> Dict[int, float]:
        weight_dict = {index: x.weight for index, x in enumerate(self.cls_info_list)}
        return weight_dict


def class_info_list_factory(class_list: List[Union[str, dict]]) -> ClsClassInfoList:
    ret_list: List[ClsClassInfo] = []
    for cls in class_list:
        if type(cls) is str:
            ret_list.append(ClsClassInfo(name=cls))
        elif type(cls) is dict:
            ret_list.append(ClsClassInfo(**cls))
    return ClsClassInfoList(ret_list)


def generate_shuffeled_class_indexes(
    cls_info_list: ClsClassInfoList,
    image_info_list: List[ClsDataInfo],
    reweight_occurrences: bool,
) -> List[int]:
    if not cls_info_list.has_custom_weighting() and not reweight_occurrences:
        index_list = list(range(len(image_info_list)))
        random.shuffle(index_list)
        return index_list

    class_idx_dict = defaultdict(list)
    for idx, image_info in enumerate(image_info_list):
        for class_idx in image_info.get_index_list():
            class_idx_dict[class_idx].append(idx)

    occurences = {key: len(value) for key, value in class_idx_dict.items()}

    max_occurences = np.max(list(occurences.values()))

    class_weights = cls_info_list.get_class_weights()
    if reweight_occurrences:
        class_weights = {
            index: max_occurences / actual_occurences
            for index, actual_occurences in occurences.items()
        }

    index_list = []
    for idx, class_weight in class_weights.items():
        index_list += items_from_shuffled_list(
            class_idx_dict[idx], int(round(occurences[idx] * class_weight))
        )

    random.shuffle(index_list)
    return index_list
