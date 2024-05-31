from pathlib import Path
from typing import Tuple, Type

from pydantic import ValidationError

from libraries.models.info_category import InfoCategory


def read_models[T](model_type: Type[T]) -> list[Tuple[T, Path]]:
    """Reads all models from the given directory and validates a list of models.

    Args:
        model_type: The type of the model.

    Returns:
        A list of validated models.
    """
    try:
        model_list = InfoCategory.get_info_category(model_type).get_model_info_list()
    except ValidationError as e:
        raise AssertionError(f"Failed to validation {model_type}\n{e}")
    for model, file in model_list:
        if model.id != file.parent.name:
            raise AssertionError(
                f"ID of model '{model.id.root}' does not match the directory name"
                + "'{file.path.parent.name}'"
            )
    return model_list
