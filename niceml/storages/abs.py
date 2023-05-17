import logging
import os
from typing import Dict

from niceml.data.storages.storageinterface import StorageInterface


def get_files_to_download(cloud_interface: StorageInterface, source: str, dest: str):
    """
    Download a file or directory to a path on the local filesystem

    Args:
        cloud_interface: interface to load data
        source: Source path in the container
        dest: Local destination path
    """
    logger = logging.getLogger("abs_logger")
    logger.disabled = True
    return list_download_files(cloud_interface, source, dest)


def list_download_files(
    cloud_interface: StorageInterface, bucket_path: str, local_path: str
) -> Dict[str, str]:
    """
    List all files that need to be downloaded from the given source and
    the resulting destination paths.
    Args:
        cloud_interface: interface to load data
        bucket_path: Source path in the container
        local_path: Local destination path

    Returns:
        Dictionary with the blob path as key and the local path as value
    """
    blobs = cloud_interface.list_data(bucket_path)
    download_dict = {}
    if blobs:
        for blob_path in blobs:
            file_path = os.path.relpath(blob_path, bucket_path)
            if not file_path.startswith(local_path):
                file_path = os.path.join(local_path, file_path)
            if not os.path.exists(file_path):
                download_dict[blob_path] = file_path
    else:
        download_dict[bucket_path] = local_path
    return download_dict
