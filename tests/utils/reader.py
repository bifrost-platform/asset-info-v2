from typing import Tuple, Type

from pydantic import ValidationError

from libraries.models.enum_id_type import EnumIdType
from libraries.models.enum_info import EnumInfo
from libraries.models.enum_tag_type import EnumTagType
from libraries.utils.file import File, get_model_info_list, get_enum_info


def read_models[T](model_type: Type[T]) -> list[Tuple[T, File]]:
    """Reads all models from the given directory and validates a list of models.

    Args:
        model_type: The type of the model.

    Returns:
        A list of validated models.
    """
    try:
        model_list = get_model_info_list(model_type)
    except ValidationError as e:
        raise AssertionError(f"Failed to validation {model_type}\n{e}")
    for model, file in model_list:
        if model.id != file.path.parent.name:
            raise AssertionError(
                f"ID of model '{model.id}' does not match the directory name"
                + "'{file.path.parent.name}'"
            )
    return model_list


def read_enum_info(enum_type: EnumTagType | EnumIdType) -> list[EnumInfo]:
    """Reads the enum information from the given enum type and enum name.

    Args:
        enum_type: The type of the enum.

    Returns:
        A list of enum information.
    """
    try:
        return get_enum_info(enum_type)
    except ValidationError as e:
        raise AssertionError(f"Failed to validation {enum_type}\n{e}")
