import os
from json import loads

from pydantic import ValidationError, RootModel
from typing_extensions import TypeVar, Type, Tuple

from libraries.models.enum_info import EnumInfoList, EnumInfo
from libraries.models.enum_type import EnumTypeEnum
from libraries.utils.file import search, PWD, File
from libraries.utils.model import CamelCaseModel

CamelModel = TypeVar("CamelModel", bound=CamelCaseModel)
"""A type variable for the :class:`CamelCaseModel`.""" ""


def read_models(
    model_type: Type[CamelModel], model_dir_name: str
) -> list[Tuple[CamelModel, File]]:
    """Reads all models from the given directory and returns a list of models.

    Args:
        model_type: The type of the models to read.
        model_dir_name: The name of the directory in the project to read the models from.

    Returns:
        A list of models.

    Notes:
        It only reads the `info.json` file from the given directory and its child directories.
    """
    models = []
    files = search(PWD.joinpath(model_dir_name), "info.json")
    for file in files:
        with open(file.path, "r") as fp:
            try:
                model = model_type.model_validate(loads(fp.read()))
                if model.id != file.path.parent.name:
                    raise AssertionError(
                        f"ID of model '{model.id}' does not match the directory name '{file.path.parent.name}'"
                    )
                models.append((model, file))
            except ValidationError as e:
                raise AssertionError(
                    f"Failed to validation {file.path.parent.name}@{model_dir_name}\n{e}"
                )
    return models


def read_enum_info(enum_type: EnumTypeEnum, enum_name: str) -> list[EnumInfo]:
    """Reads the enum information from the given enum type and enum name.

    Args:
        enum_type: The type of the enum.
        enum_name: The name of the enum.

    Returns:
        A list of enum information.
    """
    with open(
        os.path.join(PWD, f"enums/{enum_type.value}/{enum_name}.json"), "r"
    ) as fp:
        try:
            return RootModel[EnumInfoList].model_validate(loads(fp.read())).root
        except ValidationError as e:
            raise AssertionError(
                f"Failed to validation {enum_name}@{enum_type.value}\n{e}"
            )
