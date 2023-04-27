from tempfile import TemporaryDirectory

import pytest

from niceml.utilities.omegaconfutils import register_ccml_resolvers

register_ccml_resolvers()


@pytest.fixture()
def tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp
