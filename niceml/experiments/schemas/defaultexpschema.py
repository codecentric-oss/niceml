"""Module containing the default experiment schema"""
from os.path import join

from niceml.config.subsetnames import SubsetNames
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.experiments.schemas.baseexpschema import BaseExperimentSchema
from niceml.experiments.schemas.expmember import FolderMember
from niceml.experiments.schemas.yamlexpmember import YamlMember


class DefaultExperimentSchema(
    BaseExperimentSchema
):  # pylint: disable=too-few-public-methods
    """default experiment schema for subclassing"""

    test_analysis_file = YamlMember(
        path=join(
            ExperimentFilenames.ANALYSIS_FOLDER,
            ExperimentFilenames.ANALYSIS_FILE.format(dataset_name=SubsetNames.TEST),
        ),
        required=True,
        description="This file contains the analysis metrics of the test set.",
    )
    validation_analysis_file = YamlMember(
        path=join(
            ExperimentFilenames.ANALYSIS_FOLDER,
            ExperimentFilenames.ANALYSIS_FILE.format(
                dataset_name=SubsetNames.VALIDATION
            ),
        ),
        required=True,
        description="This file contains the analysis metrics of the validation set.",
    )
    train_eval_analysis_file = YamlMember(
        path=join(
            ExperimentFilenames.ANALYSIS_FOLDER,
            ExperimentFilenames.ANALYSIS_FILE.format(
                dataset_name=SubsetNames.TRAIN_EVAL
            ),
        ),
        required=True,
        description="This file contains the analysis metrics of the train set.",
    )
    git_versions_file = YamlMember(
        path=ExperimentFilenames.GIT_VERSIONS,
        required=True,
        description="This file contains the git versions of the used and specified packages.",
    )
    prediction_folder = FolderMember(
        ExperimentFilenames.PREDICTION_FOLDER,
        required=True,
        description="This folder contains all predictions of the datasets.",
    )
    config_folder = FolderMember(
        ExperimentFilenames.CONFIGS_FOLDER,
        required=True,
        description="This folder contains all configurations of the experiment.",
    )
