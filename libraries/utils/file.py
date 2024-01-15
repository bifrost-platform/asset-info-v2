import os
from pathlib import Path

from pydantic import BaseModel, FilePath

from libraries.utils.string import is_regex_in

# Project Works Directory: /asset-info-v2/libraries/utils/../../
PWD = Path(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))


class File(BaseModel):
    """Information about each file.

    Attributes:
        path: The path of the file. (:class:`FilePath`: constrained :class:`Path`)
        name: The name of the file. (:class:`str`)
    """
    path: FilePath
    name: str


def search(base_dir: Path, pattern: str) -> list[File]:
    """Searches for files in the given directory and its child directories.

    Args:
        base_dir: The base directory to search for files.
        pattern: The regex pattern to search for files.

    Returns:
        A list of files' information.
    """
    searched_files = []
    for (path, _, files) in os.walk(base_dir):
        searched_files.extend(
            [File(path=os.path.join(path, file), name=file) for file in files if is_regex_in(file, pattern)])
    return searched_files
