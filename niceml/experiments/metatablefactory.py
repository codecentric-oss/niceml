from typing import List, Optional

from niceml.experiments.metainfotables import DefaultMetaTable, MetaTable
from niceml.experiments.metalists import get_base_meta_list


def get_metatables_fatory(exp_type: Optional[str]) -> List[MetaTable]:
    meta_list = get_base_meta_list()

    meta_table_list = [
        DefaultMetaTable("Overview", meta_list),
        # DefaultMetaTable(
        #    "Augmentations", get_augmentations_meta_list(), list_functions=["aug"]
        # ),
    ]

    return meta_table_list
