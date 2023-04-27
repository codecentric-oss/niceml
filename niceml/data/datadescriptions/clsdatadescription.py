"""Module for ClsDataDescription"""
from dataclasses import dataclass
from typing import List, Optional, Union

from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputVectorDataDescription,
)
from niceml.utilities.imagesize import ImageSize


@dataclass
class ClsDataDescription(OutputVectorDataDescription, InputImageDataDescription):
    """DataDescription for Classification data"""

    classes: List[Union[str, dict]]  # QUEST: better naming? Explanation needed?
    target_size: ImageSize
    use_binary: bool = False
    use_multitargets: bool = False
    channel_count: int = 3

    def get_input_image_size(self) -> ImageSize:
        return self.target_size

    def get_output_size(self) -> int:
        """Returns the size of the output"""
        if self.use_binary and len(self.classes) != 2:
            raise Exception(f"Cannot use binary with {len(self.classes)} given!")
        return 1 if self.use_binary else len(self.classes)

    def get_input_channel_count(self) -> int:
        """Returns the number of input channels"""
        return self.channel_count

    def get_output_entry_names(self) -> List[str]:
        """Returns the names of the target classes"""
        class_name_list = []
        for cls in self.classes:
            if isinstance(cls, dict):
                class_name_list.append(cls["name"])
            else:
                class_name_list.append(cls)
        return class_name_list

    def get_index_for_name(
        self, name: Union[str, List[str]]
    ) -> Optional[Union[int, List[int]]]:
        """Returns the index of the given output entry name(s) as int or list of indices"""
        if isinstance(name, list):
            return super().get_index_for_name(name)
        if self.use_multitargets:
            index_list = []
            for cur_idx, cur_class in enumerate(self.classes):
                if isinstance(cur_class, dict):
                    if cur_class["name"] == name or name in cur_class.get(
                        "subclasses", []
                    ):
                        index_list.append(cur_idx)
                elif cur_class == name:
                    index_list.append(cur_idx)
            return index_list or None
        return super().get_index_for_name(name)
