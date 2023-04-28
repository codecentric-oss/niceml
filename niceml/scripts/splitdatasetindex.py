""" Split dataset index module """
from collections import defaultdict
from os import makedirs
from os.path import isdir, join
from typing import Dict, List, Tuple

import click
import fastparquet
import numpy as np
import pandas as pd

from niceml.utilities.idutils import ALPHANUMERICLIST
from niceml.utilities.splitutils import DataSetInfo, init_dataset_info


def get_set(file_id: str, set_infos: List[DataSetInfo]) -> str:
    """
    Chooses a set for a file according to the given sets with their probability.
    If you run get_set with the same arguments multiple times,
    you will always get back the same result.

    Args:
        file_id: file id
        set_infos: list of DataSetInfos including set names and their probability

    Returns:
        Name of the chosen set
    """
    identifier = "".join([x for x in file_id if x in ALPHANUMERICLIST])
    cur_seed = int(identifier, base=len(ALPHANUMERICLIST)) % (2**32 - 1)
    rng = np.random.default_rng(cur_seed)
    tmp_list: List[Tuple[str, float]] = [
        (dsf.set_name, dsf.probability) for dsf in set_infos
    ]
    names, probs = zip(*tmp_list)
    return rng.choice(list(names), 1, p=list(probs))[0]


def split_dataset_index(
    index_file: str,
    output_folder: str,
    set_infos: List[DataSetInfo],
    index_col_name: str,
):
    """Split dataset index into subsets"""
    index_df: pd.DataFrame = fastparquet.ParquetFile(index_file).to_pandas()
    set_row_dict: Dict[str, list] = defaultdict(list)
    for _, cur_row in index_df.iterrows():
        target_set = get_set(cur_row[index_col_name], set_infos)
        set_row_dict[target_set].append(cur_row)

    if not isdir(output_folder):
        makedirs(output_folder)
    for set_name, row_list in set_row_dict.items():
        cur_df = pd.DataFrame(row_list)
        fastparquet.write(join(output_folder, f"{set_name}.parq"), cur_df)


@click.command()
@click.argument("index_file")
@click.argument("output_location")
@click.argument("index_col_name")
@click.argument("set_infos", nargs=-1)
def split_dataset_index_cmd(
    index_file: str, output_folder: str, index_col_name: str, set_infos: List[str]
):
    """Split dataset index command"""
    set_prob_infos: List[DataSetInfo] = [init_dataset_info(x) for x in set_infos]
    split_dataset_index(index_file, output_folder, set_prob_infos, index_col_name)


if __name__ == "__main__":
    split_dataset_index_cmd()  # pylint: disable=no-value-for-parameter
