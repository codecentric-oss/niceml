"""Module for op crop_numbers"""
import json
from os.path import basename, dirname, join, splitext
from typing import Union

from attrs import asdict
from hydra.utils import ConvertMode, instantiate
from tqdm import tqdm

from niceml.utilities.boundingboxes.bboxlabeling import ObjDetImageLabel
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_location_w_path,
    open_location,
)
from niceml.utilities.imagegeneration import load_label_from_json
from niceml.utilities.ioutils import list_dir, read_image, write_image
from niceml.utilities.splitutils import clear_folder
from dagster import Field, OpExecutionContext, op


@op(
    config_schema={
        "output_location": Field(
            dict, description="Foldername where the images are stored"
        ),
        "name_delimiter": Field(
            str, default_value="_", description="Delimiter used within the filenames"
        ),
        "sub_dir": Field(
            str, default_value="", description="Subdirectory to save the split images"
        ),
        "recursive": Field(
            bool,
            default_value=True,
            description="Flag if the input folder should be searched recursively",
        ),
        "clear_folder": Field(
            bool,
            default_value=False,
            description="Flag if the output folder should be cleared before the split",
        ),
    }
)
def crop_numbers(  # pylint: disable=too-many-locals
    context: OpExecutionContext, input_location: dict
):
    """Crops the numbers from the input images and stores them separately"""
    op_config = json.loads(json.dumps(context.op_config))

    instantiated_op_config = instantiate(op_config, _convert_=ConvertMode.ALL)

    output_location: Union[dict, LocationConfig] = instantiated_op_config[
        "output_location"
    ]
    if len(instantiated_op_config["sub_dir"]) > 0:
        output_location = join_location_w_path(
            output_location, instantiated_op_config["sub_dir"]
        )
    if instantiated_op_config["clear_folder"]:
        clear_folder(output_location)
    name_delimiter: str = instantiated_op_config["name_delimiter"]
    recursive: bool = instantiated_op_config["recursive"]

    with open_location(input_location) as (input_fs, input_root):
        image_files = [
            cur_file
            for cur_file in list_dir(
                input_root, recursive=recursive, file_system=input_fs
            )
            if splitext(cur_file)[1] == ".png" and "mask" not in cur_file
        ]

        for cur_file in tqdm(image_files):
            label_file = f"{splitext(cur_file)[0]}.json"
            if not input_fs.isfile(join(input_root, label_file)):
                continue
            img = read_image(join(input_root, cur_file), file_system=input_fs)
            image_label: ObjDetImageLabel = load_label_from_json(
                input_location, label_file
            )
            for lbl_idx, cur_label in enumerate(image_label.labels):
                class_name = cur_label.class_name
                file_id = basename(splitext(cur_file)[0])
                crop_box = cur_label.bounding_box.get_absolute_ullr(convert_to_int=True)
                number_image = img.crop(crop_box)
                cur_out_folder = dirname(cur_file)
                out_filename = (
                    f"{file_id}{name_delimiter}{lbl_idx:03d}"
                    f"{name_delimiter}{class_name}.png"
                )
                with open_location(output_location) as (output_fs, output_root):
                    write_image(
                        number_image,
                        join(output_root, cur_out_folder, out_filename),
                        file_system=output_fs,
                    )

    if isinstance(output_location, LocationConfig):
        output_location = asdict(output_location)

    return output_location
