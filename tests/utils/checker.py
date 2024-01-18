import os
from pathlib import Path

from PIL import Image
from svgpathtools import svg2paths2

from libraries.models.image_info import ImageInfo
from libraries.models.image_type import ImageTypeEnum
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


def __check_image_existence(image_path: Path, existence: bool) -> None:
    """Check if image exists.

    Args:
        image_path: Path of the image.
        existence: File object of the image.
    """
    if existence:
        assert os.path.isfile(image_path)
    else:
        assert not os.path.isfile(image_path)


def __check_image_size(image_type: ImageTypeEnum, image_path: Path) -> None:
    """Check if image size is correct.

    Args:
        image_type: Type of the image.
        image_path: Path of the image.
    """
    if image_type.is_png():
        with Image.open(image_path) as img:
            assert img.size[0] == image_type.get_size()
            assert img.size[1] == image_type.get_size()
    elif image_type.is_svg():
        _, _, attributes = svg2paths2(image_path)
        assert int(attributes["width"]) == image_type.get_size()
        assert int(attributes["height"]) == image_type.get_size()
    else:
        raise AssertionError(f"Unknown image type: {image_type}")


def __check_image_preprocessed(image_info: ImageInfo) -> None:
    """Check if all images are preprocessed.

    Args:
        image_info: Information of image.
    """
    exist_images = [
        idx
        for idx, image_type in enumerate(ImageTypeEnum.get_ascending_type_list())
        if image_info.model_dump()[image_type.value]
    ]
    max_image = 0 if len(exist_images) == 0 else max(exist_images) + 1
    assert len(exist_images) == max_image


def check_images_validity(image_info: ImageInfo, file: File) -> None:
    """Check if all images are valid.

    Args:
        image_info: Information of image.
        file: File object of the image.
    """
    __check_image_preprocessed(image_info)
    for image, existence in image_info.model_dump().items():
        image_type = ImageTypeEnum(image)
        image_path = image_type.get_path(file.path.parent)
        __check_image_existence(image_path, existence)
        if existence:
            __check_image_size(image_type, image_path)
