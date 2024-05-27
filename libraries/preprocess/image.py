import os
from pathlib import Path

import cairosvg
from PIL import Image

from libraries.models.image_type import ImageTypeEnum
from libraries.utils.file import search, File

PNG_SIZES: list[ImageTypeEnum] = [
    typ for typ in ImageTypeEnum.get_descending_type_list() if typ.is_png()
]


def __png_to_square(img: Image) -> tuple[Image, int]:
    """Converts the PNG image to a square image.

    Args:
        img: The PNG image.

    Returns:
        The square image and the size of the square image.
    """
    if img.size[0] == img.size[1]:
        return img, img.size[0]
    size = max(img.size)
    return (
        Image.new(
            "RGBA",
            (size, size),
            (255, 255, 255, 0),
        ),
        size,
    )


def downscale_png(
    dir_path: Path, png_path: Path, overwrite: bool = True
) -> list[ImageTypeEnum]:
    """Downscales the PNG image in the given directory.

    Args:
        dir_path: The directory path to save the downscaled PNG image.
        png_path: The PNG image path to downscale.
        overwrite: Whether to overwrite the downscaled PNG image.

    Returns:
        The size list of the downscaled PNG image.
    """
    downloaded_type = []
    with Image.open(png_path) as img:
        squared_img, img_size = __png_to_square(img)
        target_sizes = [
            size.get_size() for size in PNG_SIZES if size.get_size() <= img_size
        ]
        for size in target_sizes:
            new_png_path = ImageTypeEnum.get_png_image_type(size).get_path(dir_path)
            if overwrite or not os.path.isfile(new_png_path):
                new_img = squared_img.resize((size, size))
                new_img.save(new_png_path, "png", optimize=True)
                downloaded_type.append(ImageTypeEnum.get_png_image_type(size))
    return downloaded_type


def __convert_png_to_downscaled(png_path: Path) -> None:
    """Downscales the PNG image.

    Args:
        png_path: The path of the PNG image.

    Notes:
        The PNG image is downscaled to two squared times smaller than the original
        image size (minimum: 32x32).
    """
    image_type = ImageTypeEnum.get_image_type(png_path)
    if image_type.is_png():
        downscale_png(png_path.parent, png_path)


def __convert_svg_to_png256(svg_path: Path) -> None:
    """Converts SVG image to a 256x256 PNG image.

    Args:
        svg_path: The path of the SVG image.

    Notes:
        The SVG image is converted to a 256x256 PNG image with 300 DPI.
    """
    png256_path = svg_path.parent.joinpath("image-256.png")
    if not os.path.isfile(png256_path):
        with open(svg_path, "r") as fp:
            cairosvg.svg2png(
                bytestring=fp.read(),
                write_to=str(png256_path),
                output_width=256,
                output_height=256,
                dpi=300,
                scale=2,
            )


def create_downscaled_image(base_image_path: Path) -> None:
    """Creates downscaled images.

    Args:
        base_image_path: The path of the base image.

    Raises:
        ValueError: If the type of image path is unknown.

    Notes:
        The base image path is the smallest image's path in each information directory.
    """
    match ImageTypeEnum.get_image_type(base_image_path):
        case ImageTypeEnum.SVG:
            __convert_svg_to_png256(base_image_path)
            __convert_png_to_downscaled(
                ImageTypeEnum.PNG256.get_path(base_image_path.parent)
            )
        case image_type if image_type.is_png():
            __convert_png_to_downscaled(base_image_path)
        case _:
            raise ValueError(f"Unknown image path: {base_image_path}")


def get_base_image_list(base_dir: Path) -> list[File]:
    """Gets the list of base images.

    Args:
        base_dir: The base directory to search for files.

    Returns:
        The list of base images' file information.

    Notes:
        The base image is the smallest image in each information directory.
    """
    dirs_already_found = set()
    file_list = []
    for image_type in ImageTypeEnum.get_descending_type_list():
        images = search(base_dir, image_type.get_regex_pattern())
        new_images = [
            file for file in images if file.path.parent not in dirs_already_found
        ]
        file_list.extend(new_images)
        dirs_already_found.update([file.path.parent for file in new_images])
    return file_list
