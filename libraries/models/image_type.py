from enum import Enum
from pathlib import Path


class ImageTypeEnum(str, Enum):
    """Enumerated values for the different types of images.

    Attributes:
        PNG128: enumerated value for 128x128 PNG image.
        PNG256: enumerated value for 256x256 PNG image.
        PNG32: enumerated value for 32x32 PNG image.
        PNG64: enumerated value for 64x64 PNG image.
        SVG: enumerated value for SVG image.
    """

    PNG128: str = "png128"
    PNG256: str = "png256"
    PNG32: str = "png32"
    PNG64: str = "png64"
    SVG: str = "svg"

    @staticmethod
    def get_ascending_type_list() -> list["ImageTypeEnum"]:
        """Gets the list of image types in ascending order."""
        return [
            ImageTypeEnum.PNG32,
            ImageTypeEnum.PNG64,
            ImageTypeEnum.PNG128,
            ImageTypeEnum.PNG256,
            ImageTypeEnum.SVG,
        ]

    @staticmethod
    def get_descending_type_list() -> list["ImageTypeEnum"]:
        """Gets the list of image types in descending order."""
        return [
            ImageTypeEnum.SVG,
            ImageTypeEnum.PNG256,
            ImageTypeEnum.PNG128,
            ImageTypeEnum.PNG64,
            ImageTypeEnum.PNG32,
        ]

    @staticmethod
    def get_image_type(image_path: Path) -> "ImageTypeEnum":
        """Gets the image type from the image path.

        Args:
            image_path: The path of the image.

        Returns:
            The image type.

        Raises:
            ValueError: If the image type of path is unknown.
        """
        match image_path.name:
            case "image-128.png":
                return ImageTypeEnum.PNG128
            case "image-256.png":
                return ImageTypeEnum.PNG256
            case "image-32.png":
                return ImageTypeEnum.PNG32
            case "image-64.png":
                return ImageTypeEnum.PNG64
            case "image.svg":
                return ImageTypeEnum.SVG
            case _:
                raise ValueError(f"Unknown image path: {image_path}")

    @staticmethod
    def get_png_image_type(size: int) -> "ImageTypeEnum":
        """Gets the PNG image type from the size.

        Args:
            size: The size of the PNG image.

        Returns:
            The PNG image type.

        Raises:
            ValueError: If the size of PNG image is unknown.
        """
        match size:
            case 128:
                return ImageTypeEnum.PNG128
            case 256:
                return ImageTypeEnum.PNG256
            case 32:
                return ImageTypeEnum.PNG32
            case 64:
                return ImageTypeEnum.PNG64
            case _:
                raise ValueError(f"Unknown png size: {size}")

    def get_path(self, base_dir: Path) -> Path:
        """Gets the path of the image from the image type.

        Args:
            base_dir: The base directory of the image.

        Returns:
            The path of its image.

        Raises:
            ValueError: If the image type is unknown.
        """
        match self:
            case ImageTypeEnum.PNG128:
                return base_dir.joinpath("image-128.png")
            case ImageTypeEnum.PNG256:
                return base_dir.joinpath("image-256.png")
            case ImageTypeEnum.PNG32:
                return base_dir.joinpath("image-32.png")
            case ImageTypeEnum.PNG64:
                return base_dir.joinpath("image-64.png")
            case ImageTypeEnum.SVG:
                return base_dir.joinpath("image.svg")
            case _:
                raise ValueError(f"Unknown image type: {self}")

    def get_regex_pattern(self) -> str:
        """Gets the regex pattern of the image type.

        Returns:
            The regex pattern of its image.

        Raises:
            ValueError: If the image type is unknown.
        """
        match self:
            case ImageTypeEnum.PNG128:
                return r"^image-128\.png$"
            case ImageTypeEnum.PNG256:
                return r"^image-256\.png$"
            case ImageTypeEnum.PNG32:
                return r"^image-32\.png$"
            case ImageTypeEnum.PNG64:
                return r"^image-64\.png$"
            case ImageTypeEnum.SVG:
                return r"^image\.svg$"
            case _:
                raise ValueError(f"Unknown image type: {self}")

    def get_size(self) -> int:
        """Gets the size of the image type.

        Returns:
            The size of its image.

        Raises:
            ValueError: If the image type is unknown.
        """
        match self:
            case ImageTypeEnum.PNG128:
                return 128
            case ImageTypeEnum.PNG256:
                return 256
            case ImageTypeEnum.PNG32:
                return 32
            case ImageTypeEnum.PNG64:
                return 64
            case ImageTypeEnum.SVG:
                return 128
            case _:
                raise ValueError(f"Unknown image type: {self}")

    def is_png(self) -> bool:
        """Checks if the image type is PNG.

        Returns:
            True if the image type is PNG, False otherwise.

        Raises:
            ValueError: If the image type is unknown.
        """
        match self:
            case ImageTypeEnum.PNG128 | ImageTypeEnum.PNG256 | ImageTypeEnum.PNG32 | ImageTypeEnum.PNG64:
                return True
            case ImageTypeEnum.SVG:
                return False
            case _:
                raise ValueError(f"Unknown image type: {self}")

    def is_svg(self) -> bool:
        """Checks if the image type is SVG.

        Returns:
            True if the image type is SVG, False otherwise.

        Raises:
            ValueError: If the image type is unknown.
        """
        match self:
            case ImageTypeEnum.PNG128 | ImageTypeEnum.PNG256 | ImageTypeEnum.PNG32 | ImageTypeEnum.PNG64:
                return False
            case ImageTypeEnum.SVG:
                return True
            case _:
                raise ValueError(f"Unknown image type: {self}")
