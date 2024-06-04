from typing import Type

from libraries.models.abstractions.info_model import InfoModel
from libraries.models.asset import Asset
from libraries.models.network import Network
from libraries.models.protocol import Protocol
from libraries.preprocess.enum_info import update_id_enum
from libraries.preprocess.image import get_base_image_list, create_downscaled_image


def run_image_preprocess[T: InfoModel](model_type: Type[T]) -> None:
    """Create downscaled images in all subdirectories of asset, network and protocol.

    Args:
        model_type: The type of the model.
    """
    image_path_list = get_base_image_list(
        model_type.get_info_category().get_model_dir_path()
    )
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
