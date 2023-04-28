from os.path import join
from typing import List

from niceml.config import envconfig as envc
from niceml.experiments.confextractionmetafunction import (
    ConfigInfoExtractor,
    DictKeysToStringFormatFunc,
    hydra_instance_format,
    list_type_format_func,
    rsplit_format_func,
    str_or_type_format_func,
)
from niceml.experiments.metafunctions import (
    EpochsExtractor,
    ExperimentIdExtraction,
    ExperimentInfoExtraction,
    MetaFunction,
    ModelExtractor,
)

LOSS_PATH = ["learner", "model_compiler", "loss"]
OPTIMIZER_PATH = [
    "learner",
    "model_compiler",
    "optimizer",
    "_target_",
]
LEARNING_RATE_PATH1 = [
    "learner",
    "model_compiler",
    "optimizer",
    "lr",
]
LEARNING_RATE_PATH2 = [
    "learner",
    "model_compiler",
    "optimizer",
    "learning_rate",
]
AUGMENTATIONS_LIST_PATH = [
    "data_train",
    "augmentator",
    "combined_augmentation_list",
]
IMAGE_SIZE_PATH = ["data_description", "image_size"]
IMAGE_SIZE_PATH2 = ["data_description", "image_input_size"]
IMAGE_SIZE_PATH3 = ["data_description", "input_image_size"]
IMAGE_SIZE_PATH4 = ["data_description", "input_image_size"]

AUGMENTATIONS_CONFIG_PATH = ["data_train", "augmentator", "combined_augmentation_list"]


def get_augmentations_meta_list() -> List[MetaFunction]:
    return [
        ExperimentIdExtraction(),
        ConfigInfoExtractor(
            "aug", AUGMENTATIONS_LIST_PATH, info_format_func=list_type_format_func
        ),
    ]


def get_base_meta_list() -> List[MetaFunction]:
    return [
        ExperimentIdExtraction(),
        ExperimentInfoExtraction(
            "start_time",
            envc.RUN_ID_KEY,
        ),
        EpochsExtractor(),
        ModelExtractor(),
        ConfigInfoExtractor(
            "image_size",
            [IMAGE_SIZE_PATH, IMAGE_SIZE_PATH2, IMAGE_SIZE_PATH3, IMAGE_SIZE_PATH4],
            info_format_func=DictKeysToStringFormatFunc(["width", "height"]),
        ),
        ConfigInfoExtractor(
            "loss", LOSS_PATH, info_format_func=str_or_type_format_func
        ),
        ConfigInfoExtractor(
            "optimizer",
            OPTIMIZER_PATH,
            info_format_func=rsplit_format_func,
        ),
        ConfigInfoExtractor(
            "lr",
            [LEARNING_RATE_PATH1, LEARNING_RATE_PATH2],
        ),
    ]


def get_semseg_meta_list() -> List[MetaFunction]:
    return get_base_meta_list() + [
        ConfigInfoExtractor(
            "iou_mask",
            [join("analysis", "result_validation"), "iou_mask"],
            use_yaml_files=True,
        ),
        ConfigInfoExtractor(
            "iou_mean",
            [join("analysis", "result_validation"), "mean_iou"],
            use_yaml_files=True,
        ),
    ]


def get_augmentation_list(max_augmentators: int = 5) -> List[MetaFunction]:
    """Includes ID and all augmentations when used with genericdatagenerator"""
    meta_functions = [ExperimentIdExtraction()]
    for idx in range(max_augmentators):
        cur_aug_conf_path = AUGMENTATIONS_CONFIG_PATH + [idx]
        meta_functions.append(
            ConfigInfoExtractor(
                f"augmentation_{idx}",
                cur_aug_conf_path,
                info_format_func=hydra_instance_format,
            )
        )
    return meta_functions
