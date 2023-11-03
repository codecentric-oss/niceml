import pytest

from niceml.filechecksumprocessors.filechecksumprocessor import remove_deleted_checksums


@pytest.fixture
def sample_checksum_dict():
    return {
        "inputs": {"file1.txt": "abc123", "file2.txt": "def456"},
        "outputs": {"file3.txt": "ghi789", "file4.txt": "jkl112"},
    }


@pytest.mark.parametrize(
    "input_files, output_files, expected_output",
    [
        (
            ["file1.txt", "file2.txt"],
            ["file3.txt"],
            {
                "inputs": {"file1.txt": "abc123", "file2.txt": "def456"},
                "outputs": {
                    "file3.txt": "ghi789",
                },
            },
        ),
    ],
)
def test_update_checksum_dict(
    sample_checksum_dict, input_files, output_files, expected_output
):
    updated_checksum_dict = remove_deleted_checksums(
        input_files, output_files, sample_checksum_dict
    )
    assert updated_checksum_dict == expected_output
