from os import remove
from os.path import isfile, join
from tempfile import TemporaryDirectory

import numpy as np
from PIL import Image

from niceml.data.dataloaders.cachedimageloader import RemoteDiskCacheImageLoader
from niceml.data.storages.localstorage import LocalStorage


def test_remote_disk_cache_image_loader():
    target_image = Image.new("RGB", (1200, 1024))
    filename = "tmp_image.png"
    with TemporaryDirectory() as orig_dir:
        target_image.save(join(orig_dir, filename))
        with TemporaryDirectory() as cache_dir:
            storage = LocalStorage(orig_dir)
            remote_loader = RemoteDiskCacheImageLoader(storage, cache_dir=cache_dir)

            np_image = remote_loader(filename)
            assert isfile(join(cache_dir, filename))
            remove(join(orig_dir, filename))
            np_image_2 = remote_loader(filename)
            assert np.array_equal(np_image, np_image_2)
