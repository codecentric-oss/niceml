from tempfile import TemporaryDirectory

import pytest

from niceml.utilities.omegaconfutils import register_niceml_resolvers

register_niceml_resolvers()


@pytest.fixture()
def tmp_dir() -> str:
    with TemporaryDirectory() as tmp:
        yield tmp
