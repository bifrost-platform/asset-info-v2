import os
from pathlib import Path

import cairosvg
from PIL import Image

from libraries.models.image_type import ImageType
from libraries.utils.file import search

PNG_SIZES: list[ImageType] = [typ for typ in ImageType.descending_list() if typ.is_png]


def __png_to_square_body(img: Image, size: int | None = None) -> tuple[Image, int]:
    """Converts the PNG image to a square image.

    Args:
        img: The PNG image.
        size: The size of the square image (If None, the maximum size of the image is used.)

    Returns:
        The square image and the size of the square image.
    """
    desired_size = size or max(img.size)
    if img.size[0] == desired_size and img.size[1] == desired_size:
        return img, desired_size
    return (
        img.resize((desired_size, desired_size), Image.LANCZOS),
        desired_size,
    )


def png_to_square(png_path: Path, dest_path: Path, size: int | None = None) -> None:
    """Converts the PNG image to a square image.

    Args:
        png_path: The PNG image path to make a square image.
        dest_path: The destination path to save the square image.
        size: The size of the square image (If None, the minimum size of png image in this system.)

    Returns:
        The path of the square image.
    """
    with Image.open(png_path) as img:
        desired_size = size or max(
            list(img.size) + [min(image_type.size for image_type in PNG_SIZES)]
        )
        img, _ = __png_to_square_body(img, desired_size)
        img.save(dest_path, "png", optimize=True)


def downscale_png(
    dir_path: Path, png_path: Path, overwrite: bool = True
) -> list[ImageType]:
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
        squared_img, img_size = __png_to_square_body(img)
        target_sizes = [
            image_type.size for image_type in PNG_SIZES if image_type.size <= img_size
        ]
        for size in target_sizes:
            new_png_path = ImageType.get_png_image_type(size).get_path(dir_path)
            if overwrite or not os.path.isfile(new_png_path):
                new_img = squared_img.resize((size, size))
                new_img.save(new_png_path, "png", optimize=True)
                downloaded_type.append(ImageType.get_png_image_type(size))
    return downloaded_type


def __convert_png_to_downscaled(png_path: Path) -> None:
    """Downscales the PNG image.

    Args:
        png_path: The path of the PNG image.

    Notes:
        The PNG image is downscaled to two squared times smaller than the original
        image size (minimum: 32x32).
    """
    image_type = ImageType.get_image_type_from_path(png_path)
    if image_type.is_png:
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
    image_type = ImageType.get_image_type_from_path(base_image_path)
    if image_type.is_svg:
        __convert_svg_to_png256(base_image_path)
        __convert_png_to_downscaled(ImageType.PNG256.get_path(base_image_path.parent))
    elif image_type.is_png:
        __convert_png_to_downscaled(base_image_path)


def get_base_image_list(base_dir: Path) -> list[Path]:
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
    for image_type in ImageType.descending_list():
        images = search(base_dir, image_type.regex_pattern)
        new_images = [file for file in images if file.parent not in dirs_already_found]
        file_list.extend(new_images)
        dirs_already_found.update([file.parent for file in new_images])
    return file_list
