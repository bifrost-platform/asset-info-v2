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


def run_preprocess() -> None:
    """Run preprocess list."""
    __run_image_preprocess()
