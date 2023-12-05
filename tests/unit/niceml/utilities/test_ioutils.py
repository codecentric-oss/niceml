import pytest
from fsspec.implementations.local import LocalFileSystem

from niceml.utilities.ioutils import list_dir


@pytest.mark.parametrize(
    "return_full_path,recursive,file_system,filter_ext,expected",
    [
        (False, False, None, None, "subdir"),
        (True, False, None, None, "subdir"),
        (False, True, None, None, "subdir/test.txt"),
        (True, True, None, None, "subdir/test.txt"),
        (False, True, None, [".txt"], "subdir/test.txt"),
        (True, True, None, [".txt"], "subdir/test.txt"),
        (False, True, None, [".csv"], None),
        (True, True, None, [".csv"], None),
        (True, True, LocalFileSystem(), [".csv"], None),
        (True, True, LocalFileSystem(), [".txt"], "subdir/test.txt"),
    ],
)
def test_list_dir_recursive(
    tmp_path, return_full_path, recursive, file_system, filter_ext, expected
):
    # Create a subdirectory and a file in it
    file_name = "test.txt"
    subdir_name = "subdir"
    subdir_path = tmp_path / subdir_name
    subdir_path.mkdir()
    file_path = subdir_path / file_name
    file_path.write_text("Hello, world!")

    # Call the function with the recursive option
    result = list_dir(
        str(tmp_path),
        return_full_path=return_full_path,
        recursive=recursive,
        file_system=file_system,
        filter_ext=filter_ext,
    )
    if not expected:
        assert [] == result
    else:
        if return_full_path:
            assert f"{tmp_path}/{expected}" in result
        else:
            assert str(expected) in result


def test_list_dir_basic(tmp_path):
    # Create a file in the temporary directory
    file_name = "test.txt"
    file_path = tmp_path / file_name
    file_path.write_text("Hello, world!")

    # Call the function with the temporary directory as the path
    result = list_dir(str(tmp_path))

    # Check that the returned list contains the file we created
    assert str(file_name) in result


def test_list_dir_filter_ext(tmp_path):
    # Create a file with a different extension
    file_path = tmp_path / "test.py"
    file_path.write_text("Hello, world!")

    # Call the function with a filter for .txt files
    result = list_dir(str(tmp_path), filter_ext=[".txt"])

    # Check that the returned list does not contain the .py file
    assert str(file_path) not in result
