"""
This module provides classes for implementing file watching and event
notification in a local filesystem.
"""

import datetime
from abc import ABC, abstractmethod
from multiprocessing import Pool
from threading import Thread
from typing import Optional, List, Dict, Union, Any

from pydantic import BaseModel

from niceml.utilities.fsspec.locationutils import LocationConfig, open_location
from niceml.utilities.ioutils import list_dir


class Event(ABC, BaseModel):
    """
    Base class for events.


    Attributes:
        data - The data associated with the event.
    """

    data: Any


class FileWatchEvent(Event):
    """
    Event class for file watch events.

    Attributes:
        data:
            - A dictionary containing information about the file event.
            - created_at: Timestamp of when the event occurred.
            - filenames: List of filenames affected by the event.
            - ... every key value pair you want
    """

    data: Dict[str, Any]


class Observer(ABC):
    """
    Abstract base class for observers.
    """

    @abstractmethod
    def trigger(self, event: Optional[Event], *args, **kwargs):
        """Trigger the observer with the provided event."""


class Watcher(ABC, Thread):
    """
    Abstract base class for watchers. Start a watcher in a new Thread to keep the main thread free.

    Attributes:
        is_watching - Flag indicating whether the watcher is actively watching.
        exception- An exception that occurred during the watch process.
    """

    def __init__(self):
        super().__init__()
        self._is_watching: bool = True
        self._exception: Optional[BaseException] = None

    def run(self):
        """
        Run the watcher's watch method in a separate thread.
        """
        try:
            self.watch()
        except BaseException as exception:
            self._exception = exception
        finally:
            self.stop()

    @abstractmethod
    def watch(self):
        """
        Abstract method to be implemented by subclasses for the actual watch logic.
        """

    def join(self, timeout: float | None = ...) -> None:
        """
        Stop the watcher.
        """
        self.stop()

    def stop(self):
        """
        Stop the watcher.
        """
        self._is_watching = False
        Thread.join(self)
        if self._exception:
            raise self._exception


class ObserverWatcher(Watcher, ABC):
    """
    Abstract base class for observers with a watcher.

    Attributes:
        sequential_observers: Flag indicating whether observers should
        be triggered sequentially.
        observer: ist of observers.
    """

    def __init__(self, sequential_observers: bool = True):
        super().__init__()
        self.sequential_observers = sequential_observers
        self.observer: List[Observer] = []

    def add_observer(self, observer: Observer):
        """
        Add an observer to the list of observers.
        """
        self.observer.append(observer)

    def notify(self, event: Union[Optional[Event], Optional[Dict[type, Event]]]):
        """
        Notify all observers with the provided event.
        """
        pool = Pool(1 if self.sequential_observers else len(self.observer))

        try:
            pool.starmap(
                self.trigger_observer, [(observer, event) for observer in self.observer]
            )
        except BaseException as exception:
            raise exception
        finally:
            pool.close()

    @staticmethod
    def trigger_observer(
        observer: Observer,
        event: Union[Optional[Event], Optional[Dict[type, Event]]],
    ):
        """
        Trigger the observer with the provided event.
        """
        if isinstance(event, Dict):
            event = event[type(observer)]
        observer.trigger(event)


class LocalFilesystemWatcher(ObserverWatcher):
    """
    Concrete implementation of ObserverWatcher for watching a local filesystem.

    Attributes:
        watch_location: The location to watch.
        recursive:Flag indicating whether to watch the location recursively.

    Example:
        ```python
        from niceml.filewatcher import LocalFilesystemWatcher, FileWatchEvent

        def custom_observer(event):
            print(f"File created: {event.data['filenames']}")

        watcher = LocalFilesystemWatcher(
            watch_location="/path/to/watched/folder",
            recursive=True,
            sequential_observers=True
        )

        watcher.add_observer(custom_observer)
        watcher.start()  # Start watching in a separate thread

        # ... your main program logic ...

        watcher.stop()  # Stop watching when done
        ```
    """

    def __init__(
        self,
        watch_location: Union[dict, LocationConfig],
        recursive: bool = False,
        sequential_observers: bool = True,
    ):
        super().__init__(sequential_observers=sequential_observers)

        self.watch_location = watch_location
        self.recursive = recursive

    def watch(self):
        """
        Watch the specified location for file changes.
        """
        with open_location(self.watch_location) as (watch_fs, watch_root):
            previous_state = set(
                list_dir(
                    path=watch_root,
                    file_system=watch_fs,
                    recursive=self.recursive,
                )
            )

            while self._is_watching:
                current_state = set(
                    list_dir(
                        path=watch_root,
                        file_system=watch_fs,
                        recursive=self.recursive,
                    )
                )
                new_files = current_state - previous_state
                if new_files:
                    self.notify(
                        FileWatchEvent(
                            data=dict(
                                created_at=datetime.datetime.timestamp(
                                    datetime.datetime.now()
                                ),
                                filenames=list(new_files),
                            )
                        )
                    )
                previous_state = current_state
