import os
from pathlib import Path

from PIL import Image
from cairosvg import svg2png, svg2svg

from libraries.models.terminals.image_type import ImageType
from libraries.utils.file import search

PNG_TYPES: list[ImageType] = [typ for typ in ImageType.descending_list() if typ.is_png]


def __png_to_square_with_minimum_size(
    img: Image, min_size: int = min(image_type.size for image_type in PNG_TYPES)
) -> tuple[Image, int]:
    """Converts the PNG image to a square image with the minimum size.

    Args:
        img: The PNG image.
        min_size: The minimum size of the square image.

    Returns:
        The square image and the size of the square image.
    """
    desired_size = max(list(img.size) + [min_size])
    if img.size[0] == desired_size and img.size[1] == desired_size:
        return img, desired_size
    return (
        img.resize((desired_size, desired_size), Image.LANCZOS),
        desired_size,
    )


def __convert_svg_to_png256(
    svg_path: Path, png_path: Path | None = None, overwrite: bool = True
) -> None:
    """Converts SVG image to a 256x256 PNG image.

    Args:
        svg_path: The path of the SVG image.
        png_path: The path of the PNG image to save.
        overwrite: Whether to overwrite the PNG image.

    Notes:
        The SVG image is converted to a 256x256 PNG image with 300 DPI.
    """
    png256_path = png_path or svg_path.parent.joinpath("image-256.png")
    if overwrite or not os.path.isfile(png256_path):
        with open(svg_path, "r") as fp:
            svg2png(
                bytestring=fp.read(),
                write_to=str(png256_path),
                output_width=256,
                output_height=256,
                dpi=300,
                scale=2,
            )


def __resize_svg_to_128(
    svg_path: Path, resized_svg_path: Path | None = None, overwrite: bool = True
) -> None:
    """Resizes the SVG image to 128x128.

    Args:
        svg_path: The path of the SVG image.
        resized_svg_path: The path of the resized SVG image.
        overwrite: Whether to overwrite the resized SVG image.
    """
    resized_svg_path = resized_svg_path or svg_path.parent.joinpath("image.svg")
    if overwrite or not os.path.isfile(resized_svg_path):
        with open(svg_path, "r") as fp:
            svg2svg(
                bytestring=fp.read(),
                write_to=str(resized_svg_path),
                output_width=128,
                output_height=128,
                dpi=72,
            )


def __reform_jpg_to_png(
    jpg_path: Path, png_path: Path | None = None, overwrite: bool = True
) -> None:
    """Reform JPG image to PNG image.

    Args:
        jpg_path: The path of the JPG image.
        png_path: The path of the PNG image to save.
        overwrite: Whether to overwrite the PNG image.
    """
    png_path = png_path or jpg_path.parent.joinpath("image.png")
    if overwrite or not os.path.isfile(png_path):
        with Image.open(jpg_path) as img:
            img.save(png_path, "png", optimize=True)


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
        squared_img, img_size = __png_to_square_with_minimum_size(img)
        target_sizes = [
            image_type.size for image_type in PNG_TYPES if image_type.size <= img_size
        ]
        for size in target_sizes:
            new_png_path = ImageType.get_png_image_type(size).get_path(dir_path)
            if overwrite or not os.path.isfile(new_png_path):
                new_img = squared_img.resize((size, size))
                new_img.save(new_png_path, "png", optimize=True)
                downloaded_type.append(ImageType.get_png_image_type(size))
    return downloaded_type


def downscale_svg(
    dir_path: Path, svg_path: Path, overwrite: bool = True
) -> list[ImageType]:
    """Downscales the SVG image in the given directory.

    Args:
        dir_path: The directory path to save the downscaled SVG and PNG image.
        svg_path: The SVG image path to downscale.
        overwrite: Whether to overwrite the downscaled SVG image.

    Returns:
        The size list of the downscaled SVG image.
    """
    __resize_svg_to_128(svg_path, dir_path.joinpath("image.svg"), overwrite)
    png_path = dir_path.joinpath("image-256.png")
    __convert_svg_to_png256(svg_path, png_path, overwrite)
    return downscale_png(dir_path, png_path, overwrite) + [ImageType.svg()]


def downscale_jpg(
    dir_path: Path, jpg_path: Path, overwrite: bool = True
) -> list[ImageType]:
    """Downscales the JPG image in the given directory.

    Args:
        dir_path: The directory path to save the downscaled JPG image.
        jpg_path: The JPG image path to downscale.
        overwrite: Whether to overwrite the downscaled JPG image.

    Returns:
        The size list of the downscaled JPG image.
    """
    png_path = dir_path.joinpath("image.png")
    __reform_jpg_to_png(jpg_path, png_path, overwrite)
    return downscale_png(dir_path, png_path, overwrite)


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
        downscale_svg(base_image_path.parent, base_image_path, overwrite=False)
    elif image_type.is_png:
        downscale_png(base_image_path.parent, base_image_path, overwrite=False)
    else:
        raise ValueError(f"Unknown image path: {base_image_path}")


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
