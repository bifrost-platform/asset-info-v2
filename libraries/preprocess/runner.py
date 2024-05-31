from typing import Type

from libraries.models.asset import Asset
from libraries.models.network import Network
from libraries.models.protocol import Protocol
from libraries.preprocess.enum_info import update_id_enum
from libraries.preprocess.image import get_base_image_list, create_downscaled_image
from libraries.utils.file import get_model_dir_path


def run_image_preprocess[T](model_type: Type[T]) -> None:
    """Create downscaled images in all subdirectories of asset, network and protocol.

    Args:
        model_type: The type of the model.
    """
    image_path_list = get_base_image_list(get_model_dir_path(model_type))
    for image_path in image_path_list:
        create_downscaled_image(image_path)


def run_enum_preprocess[T](model_type: Type[T]) -> None:
    """Update enum information from the information of asset, network and protocol.

    Args:
        model_type: The type of the model.
    """
    update_id_enum(model_type)


def run_preprocess() -> None:
    """Run a preprocessing list."""
    for model_type in [Asset, Network, Protocol]:
        run_image_preprocess(model_type)
        run_enum_preprocess(model_type)
