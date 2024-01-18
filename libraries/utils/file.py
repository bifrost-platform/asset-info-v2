import os
from json import loads
from pathlib import Path
from typing import Type, Tuple

from pydantic import RootModel

from libraries.models.enum_id_type import EnumIdTypeEnum
from libraries.models.enum_info import EnumInfoList, EnumInfo
from libraries.models.enum_tag_type import EnumTagTypeEnum
from libraries.models.file import File
from libraries.models.info_category import InfoCategoryEnum
from libraries.utils.string import is_regex_in

# Project Works Directory: /asset-info-v2/libraries/utils/../../
PWD: Path = Path(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))


def search(base_dir: Path, pattern: str) -> list[File]:
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
                File(path=os.path.join(path, file), name=file)
                for file in files
                if is_regex_in(file, pattern)
            ]
        )
    return searched_files


def get_model_dir_path[T](model_type: Type[T]) -> Path:
    """Gets the model directory from the given model type.

    Args:
        model_type: The type of the model.

    Returns:
        The model directory.
    """
    return PWD.joinpath(InfoCategoryEnum.get_info_category(model_type))


def get_enum_path(enum_type: EnumTagTypeEnum | EnumIdTypeEnum) -> Path:
    """Gets the enum type from the given enum type.

    Args:
        enum_type: The type of the enum.

    Returns:
        The enum type.
    """
    match enum_type:
        case EnumTagTypeEnum():
            return (
                PWD.joinpath("enums")
                .joinpath("tags")
                .joinpath(f"{enum_type.value}.json")
            )
        case EnumIdTypeEnum():
            return (
                PWD.joinpath("enums")
                .joinpath("ids")
                .joinpath(f"{enum_type.value}.json")
            )
        case _:
            raise ValueError(f"Unknown enum type: {enum_type}")


def __get_model_info[T](model_type: Type[T], file_path: File) -> Tuple[T, File]:
    """Gets the model information from the given model type and file path.

    Args:
        model_type: The type of the model.
        file_path: The path of the model.

    Returns:
        The model information.
    """
    with open(file_path.path, "r") as fp:
        return (
            model_type.model_validate(loads(fp.read())),
            file_path,
        )


def get_model_info_list[T](model_type: Type[T]) -> list[Tuple[T, File]]:
    """Reads all models from the given directory and returns a list of models.

    Args:
        model_type: The type of the model.

    Returns:
        A list of models.

    Notes:
        It only reads the `info.json` file from the given type's directory and
        its child directories.
    """
    return [
        __get_model_info(model_type, file)
        for file in search(get_model_dir_path(model_type), r"^info\.json$")
    ]


def get_enum_info(enum_type: EnumTagTypeEnum | EnumIdTypeEnum) -> list[EnumInfo]:
    """Reads the enum information from the given enum type and enum name.

    Args:
        enum_type: The type of the enum.

    Returns:
        A list of enum information.
    """
    with open(get_enum_path(enum_type), "r") as fp:
        return RootModel[EnumInfoList].model_validate(loads(fp.read())).root
