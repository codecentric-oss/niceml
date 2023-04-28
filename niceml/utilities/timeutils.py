"""Module for time related utilities"""
from datetime import datetime


def generate_timestamp() -> str:
    """Generates the timestamp to be used by versioning

    Returns:
        String representation of the current timestamp
    """
    current_ts = datetime.now()
    fmt = (
        "{d.year:04d}-{d.month:02d}-{d.day:02d}T{d.hour:02d}"
        ".{d.minute:02d}.{d.second:02d}.{ms:03d}Z"
    )
    return fmt.format(d=current_ts, ms=current_ts.microsecond // 1000)
