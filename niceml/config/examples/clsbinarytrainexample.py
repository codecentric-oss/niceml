import os
from os.path import join

from niceml.config.config import InitConfig
from niceml.data.datadescriptions.clsdatadescription import ClsDataDescription
from niceml.data.datainfolistings.clsdatainfolisting import DirClsDataInfoListing
from niceml.data.dataloaders.clsdataloader import ClsDataLoader
from niceml.dlframeworks.keras.datasets.kerasgenericdataset import KerasGenericDataset
from niceml.mlcomponents.targettransformer.imageinputtransformer import (
    ImageInputTransformer,
)
from niceml.mlcomponents.targettransformer.targettransformercls import (
    TargetTransformerClassification,
)
from niceml.utilities.imagesize import ImageSize

data_description = ClsDataDescription(
    classes=["0", "1", "2", "3"],
    target_size=ImageSize(width=1024, height=1024),
)

ConfDirClsDataInfoListing = InitConfig.create_conf_from_class(DirClsDataInfoListing)
ConfClsDataLoader = InitConfig.create_conf_from_class(ClsDataLoader)
ConfImageInputTransformer = InitConfig.create_conf_from_class(ImageInputTransformer)
ConfTargetTransformerClassification = InitConfig.create_conf_from_class(
    TargetTransformerClassification
)


dataset_train = InitConfig.create(
    KerasGenericDataset,
    batch_size=16,
    set_name="train",
    shuffle=True,
    datainfo_listing=ConfDirClsDataInfoListing(
        location=dict(uri=join(os.getenv("DATA_URI"), "number_data_split")),
        sub_dir="train",
    ),
    data_loader=ConfClsDataLoader(data_description=data_description),
    target_transformer=ConfTargetTransformerClassification(
        data_description=data_description
    ),
    input_transformer=ConfImageInputTransformer(data_description=data_description),
    net_data_logger=None,
)
