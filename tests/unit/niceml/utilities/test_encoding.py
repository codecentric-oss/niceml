from os.path import join
from tempfile import TemporaryDirectory

import numpy as np
import pytest
from PIL import Image

from niceml.utilities.encoding import (
    base64_to_bytesio,
    get_base64_from_file,
    numpy_to_base64,
)


@pytest.fixture
def test_text() -> str:
    return "This is a testfile"


@pytest.fixture
def test_file(test_text: str):
    with TemporaryDirectory() as tmp:
        outfile = join(tmp, "test.txt")
        with open(outfile, "w") as file:
            file.write(test_text)
        yield outfile


def test_get_base64_from_file(test_file: str):
    b_64 = get_base64_from_file(test_file)
    target = b"VGhpcyBpcyBhIHRlc3RmaWxl"
    assert b_64 == target


def test_get_base64_from_empty_file():
    with TemporaryDirectory() as tmp:
        outfile = join(tmp, "test.txt")
        open(outfile, "w").close()
        b_64 = get_base64_from_file(outfile)
        assert b_64 == b""


def test_base64_to_bytesio(test_file: str, test_text: str):
    b_64 = get_base64_from_file(test_file)
    with base64_to_bytesio(b_64) as f:
        text = f.read().decode("utf-8")
    assert text == test_text


def test_numpy_to_bas64():
    array = np.ones((10, 15), dtype=np.uint8) * 5
    b_64: str = numpy_to_base64(array)
    with base64_to_bytesio(b_64) as f:
        new_img = Image.open(f)
        new_array = np.array(new_img)
        assert np.array_equal(array, new_array)
