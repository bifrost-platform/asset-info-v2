import json
from typing import Type

from libraries.models.abstractions.info_model import InfoModel
from libraries.models.enum_info import EnumInfo


def __get_id_enum_from_model[T: InfoModel](model_type: Type[T]) -> list[EnumInfo]:
    """Gets the enum information from the given model type.

    Args:
        model_type: The type of the model.

    Returns:
        The enum information.
    """
    return sorted(
        [
            EnumInfo(value=model.id, description=model.name)
            for model, _ in model_type.get_info_list()
        ],
        key=lambda x: x.value,
    )


def update_id_enum[T: InfoModel](model_type: Type[T]) -> None:
    """Updates the enum information from the given model type.

    Args:
        model_type: The type of the model.
    """
    enum_info_list = [
        model.model_dump(mode="python")
        for model in __get_id_enum_from_model(model_type)
    ]
    with open(
        model_type.get_info_category().get_enum_type().get_enum_path(),
        "w",
    ) as fp:
        json.dump(enum_info_list, fp, indent=2)
        fp.write("\n")
