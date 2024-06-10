from json import load, dump
from typing import Type

from libraries.models.abstractions.info_model import InfoModel
from libraries.utils.file import search


def update_info[T: InfoModel](model_type: Type[T]) -> None:
    """Update the information of the model type.

    Args:
        model_type: The type of the model.
    """
    for file_path in search(
        model_type.get_info_category().get_model_dir_path(), r"^info\.json$"
    ):
        with open(file_path, "r") as fp:
            info = model_type.model_validate(load(fp))
        with open(file_path, "w") as fp:
            dump(
                info.model_dump(mode="json", by_alias=True),
                fp,
                indent=2,
                sort_keys=True,
            )
            fp.write("\n")
