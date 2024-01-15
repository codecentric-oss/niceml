import datetime
import time
from collections import defaultdict
from os.path import join, splitext
from tempfile import TemporaryDirectory
from threading import Thread
from typing import Optional, List, Union

import numpy as np
import pytest
from PIL import Image

from niceml.utilities.fsspec.locationutils import (
    open_location,
    join_fs_path,
    LocationConfig,
)
from niceml.utilities.watcher import (
    Observer,
    Event,
    FileWatchEvent,
    LocalFilesystemWatcher,
)
from niceml.utilities.ioutils import (
    write_image,
    write_yaml,
    read_yaml,
)


class TestObserver(Observer):
    def __init__(self, id: int, check_file_dir: str):
        self.id = id
        self.check_file_dir = check_file_dir

    def trigger(self, event: Optional[Event], *args, **kwargs):
        if isinstance(event, FileWatchEvent):
            with open_location(dict(uri=self.check_file_dir)) as (
                check_file_fs,
                check_file_root,
            ):
                try:
                    check_file = read_yaml(
                        filepath=join_fs_path(
                            check_file_fs, check_file_root, "check_file.yaml"
                        )
                    )
                except FileNotFoundError:
                    check_file = {}

                check_file = defaultdict(list, check_file)
                check_file[self.id].append(
                    dict(
                        triggered_at=event.data["created_at"],
                        new_files=event.data["filenames"],
                    )
                )
                write_yaml(
                    dict(check_file),
                    filepath=join_fs_path(
                        check_file_fs, check_file_root, "check_file.yaml"
                    ),
                    file_system=check_file_fs,
                )
                return

        raise ValueError


class TestLocalFilesystemWatcher:
    @pytest.fixture()
    def tmp_dir(self) -> str:
        with TemporaryDirectory() as tmp:
            yield tmp

    @pytest.fixture
    def observer(self, tmp_dir) -> List[TestObserver]:
        return [
            TestObserver(1, join(tmp_dir, "check_file")),
            TestObserver(2, join(tmp_dir, "check_file")),
        ]

    @pytest.fixture
    def watcher(self, tmp_dir, observer) -> LocalFilesystemWatcher:
        watcher = LocalFilesystemWatcher(
            watch_location=dict(uri=join(tmp_dir)),
            sequential_observers=True,
        )
        for cur_observer in observer:
            watcher.add_observer(cur_observer)
        return watcher

    def test_watch(self, watcher, tmp_dir):
        data_creation_thread = Thread(
            target=create_data,
            args=[watcher.watch_location],
        )
        watcher.start()

        data_creation_thread.start()
        data_creation_thread.join()

        with open_location(watcher.watch_location) as (
            check_file_fs,
            check_file_root,
        ):
            time.sleep(10)
            check_file = read_yaml(
                join_fs_path(
                    check_file_fs, check_file_root, "check_file", "check_file.yaml"
                )
            )
            assert len(watcher.observer) == len(check_file)
            for observer in check_file.values():
                checked_files_count = 0
                for entry in observer:
                    for file in entry["new_files"]:
                        created_at = splitext(file)[0]
                        if file == "check_file":
                            continue
                        checked_files_count += 1
                        delta = datetime.datetime.fromtimestamp(
                            float(entry["triggered_at"])
                        ) - datetime.datetime.fromtimestamp(float(created_at))
                        assert delta <= datetime.timedelta(seconds=3)
                assert checked_files_count == 5
            watcher.stop()


def create_data(location: Union[LocationConfig, dict]):
    with open_location(location) as (location_fs, location_root):
        for idx in range(5):
            creation_timestamp = datetime.datetime.now().timestamp()
            img = np.zeros((1024, 1024, 3), dtype=np.uint8)
            write_image(
                image=Image.fromarray(img),
                file_system=location_fs,
                filepath=join_fs_path(
                    location_fs, location_root, f"{creation_timestamp}.png"
                ),
            )
            time.sleep(7)
