from os.path import join, splitext

import numpy as np

from niceml.data.datadescriptions.clsdatadescription import ClsDataDescription
from niceml.data.datainfolistings.clsdatainfolisting import (
    DirClsDataInfoListing,
    LabelClsDataInfoListing,
)
from niceml.utilities.fsspec.locationutils import get_location_uri
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.ioutils import list_dir


def test_clsdatainfolisting(numbers_cropped_split_dir):
    # pylint: disable=use-dict-literal
    data_info_listing_test = DirClsDataInfoListing(
        location=dict(uri=numbers_cropped_split_dir), sub_dir="test"
    )
    # pylint: disable=use-dict-literal
    data_info_listing_train = DirClsDataInfoListing(
        location=dict(uri=numbers_cropped_split_dir), sub_dir="train"
    )
    # pylint: disable=use-dict-literal
    data_info_listing_validation = DirClsDataInfoListing(
        location=dict(uri=numbers_cropped_split_dir), sub_dir="validation"
    )

    data_description = ClsDataDescription(
        classes=["0", "1", "2"], target_size=ImageSize(64, 64)
    )

    listed_images_test = data_info_listing_test.list(data_description)
    listed_images_train = data_info_listing_train.list(data_description)
    listed_images_validation = data_info_listing_validation.list(data_description)
    for cur_image in (
        listed_images_test + listed_images_validation + listed_images_train
    ):
        assert get_location_uri(cur_image.image_location).endswith(".png")
        assert cur_image.class_name in ["0", "1", "2"]

    identifiers_test = [
        splitext(data_info.identifier)[0].rsplit("_", 2)[0]
        for data_info in listed_images_test
    ]
    identifiers_train = [
        splitext(data_info.identifier)[0].rsplit("_", 2)[0]
        for data_info in listed_images_train
    ]
    identifiers_validation = [
        splitext(data_info.identifier)[0].rsplit("_", 2)[0]
        for data_info in listed_images_validation
    ]

    assert all(identifier not in identifiers_train for identifier in identifiers_test)
    assert all(
        identifier not in identifiers_validation for identifier in identifiers_test
    )
    assert all(
        identifier not in identifiers_train for identifier in identifiers_validation
    )


# pylint: disable = too-many-locals
def test_labelclsdatainfolisting(obj_det_split_dir):
    # pylint: disable=use-dict-literal
    data_info_listing_test = LabelClsDataInfoListing(
        data_location=dict(uri=obj_det_split_dir), sub_dir="test"
    )
    # pylint: disable=use-dict-literal
    data_info_listing_train = LabelClsDataInfoListing(
        data_location=dict(uri=obj_det_split_dir), sub_dir="train"
    )
    # pylint: disable=use-dict-literal
    data_info_listing_validation = LabelClsDataInfoListing(
        data_location=dict(uri=obj_det_split_dir), sub_dir="validation"
    )
    data_description = ClsDataDescription(
        classes=["0", "1", "2"], target_size=ImageSize(64, 64)
    )

    listed_images_test = data_info_listing_test.list(data_description)
    listed_images_train = data_info_listing_train.list(data_description)
    listed_images_validation = data_info_listing_validation.list(data_description)

    for cur_image in (
        listed_images_test + listed_images_validation + listed_images_train
    ):
        assert get_location_uri(cur_image.image_location).endswith(".png")
        for cur_class in cur_image.class_name:
            assert cur_class in ["0", "1", "2"]

    test_files = list_dir(join(obj_det_split_dir, "test"))
    identifiers_test = [
        splitext(file)[0] if "mask" not in file else splitext(file)[0].rsplit("_", 1)[0]
        for file in test_files
    ]

    train_files = list_dir(join(obj_det_split_dir, "train"))
    identifiers_train = [
        splitext(file)[0] if "mask" not in file else splitext(file)[0].rsplit("_", 1)[0]
        for file in train_files
    ]
    validation_files = list_dir(join(obj_det_split_dir, "validation"))
    identifiers_validation = [
        splitext(file)[0] if "mask" not in file else splitext(file)[0].rsplit("_", 1)[0]
        for file in validation_files
    ]

    identifier_counts_test = np.unique(identifiers_test, return_counts=True)
    identifier_counts_train = np.unique(identifiers_train, return_counts=True)
    identifier_counts_validation = np.unique(identifiers_validation, return_counts=True)

    for cur_identifiers in [
        identifier_counts_test[1],
        identifier_counts_train[1],
        identifier_counts_validation[1],
    ]:
        assert np.unique(cur_identifiers) == 3

    assert (
        np.unique(
            list(identifier_counts_validation[1])
            + list(identifier_counts_train[1])
            + list(identifier_counts_test[1])
        )
        == 3
    )
