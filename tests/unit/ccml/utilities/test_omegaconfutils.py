import pytest
from omegaconf import OmegaConf

from niceml.utilities.omegaconfutils import register_ccml_resolvers


@pytest.mark.parametrize(
    "input,target",
    [
        ('${niceml.extract_int:"124,127",1}', 127),
        ("${niceml.extract_float:'124,127',1}", 127),
        ('${niceml.extract_float:"124.4,127",0}', 124.4),
        ('${niceml.extract_float:"124.4,127",-2}', 124.4),
        ('${niceml.extract_raw:"124.4,127",0}', "124.4"),
        ("${niceml.to_int:124}", 124),
        ("${niceml.to_int:124.2}", 124),
        ("${niceml.to_float:124.2}", 124.2),
        ("${niceml.true_div:10,2}", 5),
        ("${niceml.true_div:11,2}", 5),
        ("${niceml.true_div:12.0,2.1}", 5),
    ],
)
def test_str_sep_resolver(input: str, target):
    cfg = OmegaConf.create(dict(target=input))
    assert cfg.target == target


def test_register_resolvers_multiple_times():
    register_ccml_resolvers()
    register_ccml_resolvers()
