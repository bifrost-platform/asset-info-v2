import os
from pathlib import Path

from libraries.utils.string import is_regex_in

# Project Works Directory: /asset-info-v2/libraries/utils/../../
PWD: Path = Path(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))


def search(base_dir: Path, pattern: str) -> list[Path]:
    """Searches for files in the given directory and its child directories.

    Args:
        base_dir: The base directory to search for files.
        pattern: The regex pattern to search for files.

    Returns:
        A list of files' information.
    """
    searched_files = []
    for path, _, files in os.walk(base_dir):
        searched_files.extend(
            [
                Path(os.path.join(path, file))
                for file in files
                if is_regex_in(file, pattern)
            ]
        )
    return searched_files
