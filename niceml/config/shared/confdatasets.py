from pydantic import Field

from niceml.config.config import get_class_path, InitConfig
from niceml.config.subsetnames import SubsetNames
from niceml.data.datainfolistings.clsdatainfolisting import DirClsDataInfoListing
from niceml.data.dataloaders.clsdataloader import ClsDataLoader
from niceml.dlframeworks.keras.datasets.kerasgenericdataset import KerasGenericDataset
from niceml.mlcomponents.targettransformer.imageinputtransformer import (
    ImageInputTransformer,
)
from niceml.mlcomponents.targettransformer.targettransformercls import (
    TargetTransformerClassification,
)


class ConfDirClsDataInfoListingTest(InitConfig):
    """This class configures the data info listing"""

    target: str = InitConfig.create_target_field(DirClsDataInfoListing)
    location: dict = dict(uri="uri: ${oc.env:DATA_URI,./data}/numbers_cropped_split")
    sub_dir: str = SubsetNames.TEST


class ConfDatasetClsTest(InitConfig):
    """This class configures the dataset"""

    target: str = InitConfig.create_target_field(KerasGenericDataset)
    set_name: str = SubsetNames.TEST
    batch_size: int = 2
    shuffle: bool = False
    datainfo_listing: ConfDirClsDataInfoListingTest = Field(
        default_factory=ConfDirClsDataInfoListingTest
    )
    data_loader: InitConfig = InitConfig(_target_=get_class_path(ClsDataLoader))
    target_transformer: InitConfig = InitConfig(
        _target_=get_class_path(TargetTransformerClassification)
    )
    input_transformer: InitConfig = InitConfig(
        _target_=get_class_path(ImageInputTransformer)
    )


class ConfDirClsDataInfoListingTrain(ConfDirClsDataInfoListingTest):
    """This class configures the data info listing"""

    sub_dir: str = SubsetNames.TRAIN


class ConfDatasetClsTrain(ConfDatasetClsTest):
    """This class configures the dataset for training"""

    set_name: str = SubsetNames.TRAIN
    shuffle: bool = True
    datainfo_listing: ConfDirClsDataInfoListingTrain = Field(
        default_factory=ConfDirClsDataInfoListingTrain
    )


class ConfDirClsDataInfoListingValidation(ConfDirClsDataInfoListingTest):
    """This class configures the data info listing"""

    sub_dir: str = SubsetNames.VALIDATION


class ConfDatasetClsValidation(ConfDatasetClsTest):
    """This class configures the dataset for validation"""

    set_name: str = SubsetNames.VALIDATION
    datainfo_listing: ConfDirClsDataInfoListingValidation = Field(
        default_factory=ConfDirClsDataInfoListingValidation
    )
