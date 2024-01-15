import os

from libraries.models.image_info import ImageInfo
from libraries.utils.file import File, PWD


def check_info_json_existence(model_dir_name: str) -> None:
    """Check if all directories in subdirectory of `model_dir_name` has a `info.json` file.

    Args:
        model_dir_name: Name of the directory which contains directories for models.
    """
    model_dir = PWD.joinpath(model_dir_name)
    for name in os.listdir(model_dir):
        sub_dir = model_dir.joinpath(name)
        if not os.path.isdir(sub_dir):
            continue
        assert os.path.exists(sub_dir.joinpath("info.json"))


def check_png128(image_info: ImageInfo, file: File) -> None:
    """Check if 128x128 png image exists if `png128` of :class:`ImageInfo` is `True`.

    Args:
        image_info: Information of image.
        file: File object of the image.
    """
    if image_info.png128:
        assert os.path.isfile(file.path.parent.joinpath("image-128.png"))
    else:
        assert not os.path.isfile(file.path.parent.joinpath("image-128.png"))


def check_png256(image_info: ImageInfo, file: File) -> None:
    """Check if 256x256 png image exists if `png256` of :class:`ImageInfo` is `True`.

    Args:
        image_info: Information of image.
        file: File object of the image.
    """
    if image_info.png256:
        assert os.path.isfile(file.path.parent.joinpath("image-256.png"))
    else:
        assert not os.path.isfile(file.path.parent.joinpath("image-256.png"))


def check_png32(image_info: ImageInfo, file: File) -> None:
    """Check if 32x32 png image exists if `png32` of :class:`ImageInfo` is `True`.

    Args:
        image_info: Information of image.
        file: File object of the image.
    """
    if image_info.png32:
        assert os.path.isfile(file.path.parent.joinpath("image-32.png"))
    else:
        assert not os.path.isfile(file.path.parent.joinpath("image-32.png"))


def check_png64(image_info: ImageInfo, file: File) -> None:
    """Check if 64x64 png image exists if `png64` of :class:`ImageInfo` is `True`.

    Args:
        image_info: Information of image.
        file: File object of the image.
    """
    if image_info.png64:
        assert os.path.isfile(file.path.parent.joinpath("image-64.png"))
    else:
        assert not os.path.isfile(file.path.parent.joinpath("image-64.png"))


def check_svg(image_info: ImageInfo, file: File) -> None:
    """Check if svg image exists if `svg` of :class:`ImageInfo` is `True`.

    Args:
        image_info: Information of image.
        file: File object of the image.
    """
    if image_info.svg:
        assert os.path.isfile(file.path.parent.joinpath("image.svg"))
    else:
        assert not os.path.isfile(file.path.parent.joinpath("image.svg"))


def check_images_validity(image_info: ImageInfo, file: File) -> None:
    """Check if all images are valid.

    Args:
        image_info: Information of image.
        file: File object of the image.
    """
    check_png128(image_info, file)
    check_png256(image_info, file)
    check_png32(image_info, file)
    check_png64(image_info, file)
    check_svg(image_info, file)
