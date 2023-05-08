from niceml.dagster.ops.train import train
from niceml.mkdocs.mdop import get_md_op


def test_get_md_op():
    cur_md = get_md_op(train)
    assert len(cur_md) > 0
