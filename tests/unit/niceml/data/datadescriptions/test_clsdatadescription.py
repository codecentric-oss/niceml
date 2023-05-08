import pytest

from niceml.data.datadescriptions.clsdatadescription import ClsDataDescription
from niceml.utilities.imagesize import ImageSize


def test_get_input_image_size(cls_data_description: ClsDataDescription):
    expected_image_size = ImageSize(100, 200)
    assert expected_image_size == cls_data_description.get_input_image_size()


def test_get_output_size(cls_data_description: ClsDataDescription):
    expected_output_size = 3
    assert cls_data_description.get_output_size() == expected_output_size


def test_get_input_channel_count(cls_data_description: ClsDataDescription):
    expected_channel_count = 3
    assert expected_channel_count == cls_data_description.get_input_channel_count()


def test_get_output_entry_names(cls_data_description: ClsDataDescription):
    expected_output_entry_names = ["class1", "class2", "class3"]
    assert expected_output_entry_names == cls_data_description.get_output_entry_names()


def test_get_index_for_name(cls_data_description: ClsDataDescription):
    expected_index = 2
    assert expected_index == cls_data_description.get_index_for_name("class3")


def test_get_name_for_index(cls_data_description: ClsDataDescription):
    expected_name = "class2"
    assert expected_name == cls_data_description.get_name_for_index(1)


@pytest.fixture
def cls_data_description():
    data_desc = ClsDataDescription(
        target_size=ImageSize(100, 200),
        classes=["class1", "class2", "class3"],
        use_binary=False,
        use_multitargets=False,
        channel_count=3,
    )
    return data_desc


def test_cls_data_description_binary(cls_data_description: ClsDataDescription):
    cls_data_description.use_binary = True
    with pytest.raises(Exception):
        cls_data_description.get_output_size()


def test_cls_data_description_binary_outputsize():
    cls_data_description = ClsDataDescription(
        target_size=ImageSize(100, 200),
        classes=["class1", "class2"],
        use_binary=True,
        use_multitargets=False,
        channel_count=3,
    )
    assert cls_data_description.get_output_size() == 1


def test_cls_data_description_multitargets():
    classes = [
        "class1",
        "class2",
        "class3",
        {
            "name": "multiclass1",
            "weight": 2.0,
            "subclasses": ["class1", "class2"],
        },
    ]
    cls_data_description = ClsDataDescription(
        target_size=ImageSize(100, 200),
        classes=classes,
        use_binary=False,
        use_multitargets=True,
        channel_count=3,
    )
    assert cls_data_description.get_output_size() == 4
    assert cls_data_description.get_output_entry_names() == [
        "class1",
        "class2",
        "class3",
        "multiclass1",
    ]
    assert cls_data_description.get_index_for_name("class1") == [0, 3]
