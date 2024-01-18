from libraries.models.asset import Asset
from libraries.models.network import Network
from libraries.models.protocol import Protocol
from libraries.utils.enum_info import update_id_enum
from libraries.utils.file import PWD
from libraries.utils.image import get_base_image_list, create_downscaled_image


def __run_image_preprocess() -> None:
    """Create downscaled images in all subdirectories of asset, network and protocol."""
    image_path_list = (
        get_base_image_list(PWD.joinpath("assets"))
        + get_base_image_list(PWD.joinpath("networks"))
        + get_base_image_list(PWD.joinpath("protocols"))
    )
    for image_path in image_path_list:
        create_downscaled_image(image_path.path)


def __run_enum_preprocess() -> None:
    """Update enum information from the information of asset, network and protocol."""
    for model_type in [Asset, Network, Protocol]:
        update_id_enum(model_type)


def run_preprocess() -> None:
    """Run preprocess list."""
    __run_image_preprocess()
    __run_enum_preprocess()
