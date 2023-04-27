"""Module for common utils"""
from random import shuffle
from typing import Any, List, Tuple

import numpy as np
from pympler import asizeof


def partition_indices(totalsize: int, numberofpartitions: int) -> List[Tuple[int, int]]:
    """# QUEST: still used?
    Splits the length of an iterable (totalsize) into a given number of equal parts and
    returns the start and end indices of these parts.

    Args:
        totalsize: length of the iterable to be partitioned
        numberofpartitions: number of the partitions generated
    Returns:
        List of tuples containing the start and end indices for each partition
    """
    chunksize = totalsize // numberofpartitions
    # How many chunks need an extra 1 added to the size?
    remainder = totalsize - chunksize * numberofpartitions
    start_index = 0
    for partition_idx in range(numberofpartitions):
        end_index = start_index + chunksize + (partition_idx < remainder)
        yield start_index, end_index - 1
        start_index = end_index


def items_from_shuffled_list(item_list: list, count: int) -> list:
    """
    Generates a shuffled list of 'item_list', where 'count' is the number of items in that list.
    The order is randomized. If 'count' is smaller than len(item_list), some items won't appear
    in the output. If 'count' is equal to len(item_list), all items in item_list will appear in
    the output. If there are more than one copy of an item in the input, then it
    will also appear multiple times in the output.

    Args:
        item_list: list of items, e.g. [1,2,3,4]
        count: number of required items in the output; can be bigger than len('item_list'), e.g. 4
    Returns:
        list of items which are shuffled, e.g. [3,2,1,4]
    """
    working_item_list = item_list.copy()
    out_list = []
    complete_count, residual = divmod(count, len(working_item_list))
    for _ in range(complete_count):
        shuffle(working_item_list)
        out_list += working_item_list
    if residual > 0:
        shuffle(working_item_list)
        out_list += working_item_list[:residual]

    return out_list


def to_categorical(input_vector: np.ndarray, num_classes: int):
    """1-hot encodes a tensor"""
    return np.eye(num_classes, dtype="uint8")[input_vector]


def str_to_bool(input_value: str) -> bool:
    """Checks for common str values and interprets them as bool"""
    return input_value.lower() in {"yes", "true", "t", "1"}


def check_instance(obj_instance: Any, class_type: Any) -> Any:
    """
    Checks whether 'obj_instance' is an instance of 'class_type'.
    Returns 'obj_instance' if True. Raises TypeError if not.

    Args:
        obj_instance: Object to check the instance type for
        class_type: instance type which is expected

    Returns:
        'obj_instance' if the type is correct
    """
    if isinstance(obj_instance, class_type):
        return obj_instance
    raise TypeError(
        f"Object of class {type(obj_instance)} "
        f"is not instance of class: {class_type}"
    )


def human_readable_size(obj: Any) -> str:
    """
    Returns human-readable size in bytes of an object as string

    Args:
        obj: object to check the size for

    Returns:
        Size of the object in bytes; e.g. "1.23 GB"
    """
    size = asizeof.asizeof(obj)
    if size < 1024:
        return f"{size} bytes"
    if 1024 <= size < 1024 ** 2:
        size_kb = size / 1024
        return f"{size_kb:.2f} KB"
    if 1024 ** 2 <= size < 1024 ** 3:
        size_mb = size / 1024 ** 2
        return f"{size_mb:.2f} MB"

    size_gb = size / 1024 ** 3
    return f"{size_gb:.2f} GB"
