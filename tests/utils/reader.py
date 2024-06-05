from pathlib import Path
from typing import Type

from pydantic import ValidationError

from libraries.models.abstractions.info_model import InfoModel


def read_models[T: InfoModel](model_type: Type[T]) -> list[tuple[T, Path]]:
    """Reads all models from the given directory and validates a list of models.

    Args:
        model_type: The type of the model.

    Returns:
        A list of validated models.
    """
    try:
        model_list = model_type.get_info_list()
    except ValidationError as e:
        raise AssertionError(f"Failed to validation {model_type}\n{e}")
    for model, file in model_list:
        if model.id != file.parent.name:
            raise AssertionError(
                f"ID of model '{str(model.id)}' does not match the directory name"
                + "'{file.path.parent.name}'"
            )
    return model_list
