import json
from typing import Type

from libraries.models.enum_id_type import EnumIdType
from libraries.models.enum_info import EnumInfo
from libraries.models.info_category import InfoCategoryEnum
from libraries.utils.file import get_model_info_list, get_enum_path


def __get_id_enum_from_model[T](model_type: Type[T]) -> list[EnumInfo]:
    """Gets the enum information from the given model type.

    Args:
        model_type: The type of the model.

    Returns:
        The enum information.
    """
    return sorted(
        [
            EnumInfo(value=model.id, description=model.name)
            for model, _ in get_model_info_list(model_type)
        ],
        key=lambda x: x.value,
    )


def update_id_enum[T](model_type: Type[T]) -> None:
    """Updates the enum information from the given model type.

    Args:
        model_type: The type of the model.
    """
    enum_info_list = [
        model.model_dump() for model in __get_id_enum_from_model(model_type)
    ]
    with open(
        get_enum_path(
            EnumIdType.get_enum_type(InfoCategoryEnum.get_info_category(model_type))
        ),
        "w",
    ) as fp:
        json.dump(enum_info_list, fp, indent=2)
        fp.write("\n")
