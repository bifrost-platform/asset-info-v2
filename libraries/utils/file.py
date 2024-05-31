import os
from json import loads
from pathlib import Path
from typing import Type, Tuple

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


def get_model_info[T](model_type: Type[T], file_path: Path) -> Tuple[T, Path]:
    """Gets the model information from the given model type and file path.

    Args:
        model_type: The type of the model.
        file_path: The path of the model.

    Returns:
        The model information.
    """
    with open(file_path, "r") as fp:
        return (
            model_type.model_validate(loads(fp.read())),
            file_path,
        )
