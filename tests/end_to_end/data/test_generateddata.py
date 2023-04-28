from collections import defaultdict
from os.path import splitext

from niceml.utilities.ioutils import list_dir


def test_generated_data(
    obj_det_split_dir: str, numbers_cropped_split_dir: str, sample_count: int
):
    files = list_dir(obj_det_split_dir, recursive=True)
    png_files = [x for x in files if splitext(x)[1] == ".png"]
    json_files = [x for x in files if splitext(x)[1] == ".json"]
    assert len(png_files) == sample_count * 2
    assert len(json_files) == sample_count

    count_dict = defaultdict(int)
    for cur_file in [x for x in files if "." in x]:
        cur_file = cur_file.replace("_mask", "")
        count_dict[splitext(cur_file)[0]] += 1

    for val in count_dict.values():
        assert val == 3

    assert len(list_dir(obj_det_split_dir)) == 3

    number_files = list_dir(numbers_cropped_split_dir, recursive=True)
    assert len(number_files) >= len(json_files)
