from typing import List

import pytest

from niceml.utilities.idutils import base_10_to_n, generate_short_id, id_from_id_list


@pytest.fixture
def char_list() -> list:
    return ["a", "b", "c", "d"]


@pytest.mark.parametrize("number,target", [(0, "a"), (1, "b"), (4, "ba")])
def test_base_10_to_n(number: int, target: str, char_list: list):
    pred = base_10_to_n(number, char_list)
    assert pred == target


@pytest.mark.parametrize(
    "run_id,target_short_id",
    [("2021-12-14T11.50.24.206Z", "9nco"), ("2022-01-19T16.30.03.842Z", "zycs")],
)
def test_generate_short_id(run_id: str, target_short_id: str):
    pred = generate_short_id(run_id)
    assert pred == target_short_id


@pytest.mark.parametrize(
    "id_list,target_id",
    [
        (["id46", "asdf"], "73je"),
        ([".jkl", "--23"], "5foo"),
        (["", "4655"], "6jmy"),
    ],
)
def test_id_from_id_list(id_list: List[str], target_id: str):
    pred = id_from_id_list(id_list)
    assert pred == target_id
