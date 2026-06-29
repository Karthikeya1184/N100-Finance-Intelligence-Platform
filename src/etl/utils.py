from pathlib import Path


def ensure_directory(path: Path):

    """
    Create directory if it doesn't exist.
    """

    path.mkdir(parents=True, exist_ok=True)


def file_exists(path: Path):

    """
    Check whether a file exists.
    """

    return path.exists()