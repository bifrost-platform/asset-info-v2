from asyncio import gather

from libraries.utils.file import PWD
from libraries.utils.image import get_base_image_list, create_downscaled_image


async def __run_image_preprocess() -> None:
    """Create downscaled images in all subdirectories of asset, network and protocol."""
    image_path_list = (
        get_base_image_list(PWD.joinpath("assets"))
        + get_base_image_list(PWD.joinpath("networks"))
        + get_base_image_list(PWD.joinpath("protocols"))
    )
    await gather(
        *[create_downscaled_image(image_path.path) for image_path in image_path_list]
    )


async def run_preprocess() -> None:
    """Run preprocess lists asynchronously."""
    await gather(*[__run_image_preprocess()])
