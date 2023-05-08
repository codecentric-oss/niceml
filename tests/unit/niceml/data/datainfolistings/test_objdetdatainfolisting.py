from niceml.data.datadescriptions.objdetdatadescription import ObjDetDataDescription
from niceml.data.datainfolistings.objdetdatainfolisting import ObjDetDataInfoListing
from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel
from niceml.utilities.imagesize import ImageSize


def test_objdet_info_listing(created_test_image_path):
    # Given
    classes, output_location = created_test_image_path
    img_size = ImageSize(1024, 1024)
    data_info_listing = ObjDetDataInfoListing(location=output_location, sub_dir="")
    data_description = ObjDetDataDescription(
        featuremap_scales=[8, 16, 32, 64, 128],
        classes=classes,
        input_image_size=img_size,
        anchor_aspect_ratios=[1, 0.5, 2.0],
        anchor_scales=[1, 1.25, 1.6],
        anchor_base_area_side=4,
        box_variance=[0.1, 0.1, 0.2, 0.2],
    )

    # When
    data_info_list = data_info_listing.list(data_description=data_description)

    # Then

    for data_info in data_info_list:
        for label in data_info.labels:
            assert isinstance(label, ObjDetInstanceLabel)
            assert label.class_index == classes.index(label.class_name)
        assert data_info.class_count_in_dataset == 8

    assert len(data_info_list) == 10
