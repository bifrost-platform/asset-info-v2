from enum import StrEnum
from pathlib import Path
from typing import Self

from libraries.models.templates.enum_model import EnumModel


class _ImageTypeEnum(StrEnum):
    """Enumerated values for the different types of images.

    Attributes:
        PNG128: enumerated value for 128x128 PNG image.
        PNG256: enumerated value for 256x256 PNG image.
        PNG32: enumerated value for 32x32 PNG image.
        PNG64: enumerated value for 64x64 PNG image.
        SVG: enumerated value for SVG image.
    """

    PNG32: str = "png32"
    PNG64: str = "png64"
    PNG128: str = "png128"
    PNG256: str = "png256"
    SVG: str = "svg"


class ImageType(EnumModel[_ImageTypeEnum]):
    """An alias of `_ImageTypeEnum`."""

    @property
    def is_png128(self) -> bool:
        """Checks if the image type is 128x128 PNG.

        Returns:
            True if the image type is 128x128 PNG, False otherwise.

        Raises:
            ValueError: If the image type is unknown.
        """
        return self.root == _ImageTypeEnum.PNG128

    @property
    def is_png256(self) -> bool:
        """Checks if the image type is 256x256 PNG.

        Returns:
            True if the image type is 256x256 PNG, False otherwise.

        Raises:
            ValueError: If the image type is unknown.
        """
        return self.root == _ImageTypeEnum.PNG256

    @property
    def is_png32(self) -> bool:
        """Checks if the image type is 32x32 PNG.

        Returns:
            True if the image type is 32x32 PNG, False otherwise.

        Raises:
            ValueError: If the image type is unknown.
        """
        return self.root == _ImageTypeEnum.PNG32

    @property
    def is_png64(self) -> bool:
        """Checks if the image type is 64x64 PNG.

        Returns:
            True if the image type is 64x64 PNG, False otherwise.

        Raises:
            ValueError: If the image type is unknown.
        """
        return self.root == _ImageTypeEnum.PNG64

    @property
    def is_svg(self) -> bool:
        """Checks if the image type is SVG.

        Returns:
            True if the image type is SVG, False otherwise.

        Raises:
            ValueError: If the image type is unknown.
        """
        return self.root == _ImageTypeEnum.SVG

    @property
    def is_png(self) -> bool:
        """Checks if the image type is PNG.

        Returns:
            True if the image type is PNG, False otherwise.

        Raises:
            ValueError: If the image type is unknown.
        """
        if self.is_svg:
            return False
        elif self.is_png128 or self.is_png256 or self.is_png32 or self.is_png64:
            return True
        else:
            raise ValueError(f"Unknown image type: {self}")

    @property
    def regex_pattern(self) -> str:
        """Gets the regex pattern of the image type.

        Returns:
            The regex pattern of its image.

        Raises:
            ValueError: If the image type is unknown.
        """
        return rf"^{self.file_name.replace('.', '\\.')}$"

    @property
    def file_name(self) -> str:
        """Gets the file name of the image type.

        Returns:
            The file name of its image.

        Raises:
            ValueError: If the image type is unknown.
        """
        match self.root:
            case _ImageTypeEnum.PNG128:
                return "image-128.png"
            case _ImageTypeEnum.PNG256:
                return "image-256.png"
            case _ImageTypeEnum.PNG32:
                return "image-32.png"
            case _ImageTypeEnum.PNG64:
                return "image-64.png"
            case _ImageTypeEnum.SVG:
                return "image.svg"
            case _:
                raise ValueError(f"Unknown image type: {self}")

    @property
    def size(self) -> int:
        """Gets the size of the image type.

        Returns:
            The size of its image.

        Raises:
            ValueError: If the image type is unknown.
        """
        match self.root:
            case _ImageTypeEnum.PNG128:
                return 128
            case _ImageTypeEnum.PNG256:
                return 256
            case _ImageTypeEnum.PNG32:
                return 32
            case _ImageTypeEnum.PNG64:
                return 64
            case _ImageTypeEnum.SVG:
                return 128
            case _:
                raise ValueError(f"Unknown image type: {self}")

    @staticmethod
    def png128() -> Self:
        """Gets the enum type for 128x128 PNG image.

        Returns:
            The enum type for 128x128 PNG image.
        """
        return ImageType(_ImageTypeEnum.PNG128)

    @staticmethod
    def png256() -> Self:
        """Gets the enum type for 256x256 PNG image.

        Returns:
            The enum type for 256x256 PNG image.
        """
        return ImageType(_ImageTypeEnum.PNG256)

    @staticmethod
    def png32() -> Self:
        """Gets the enum type for 32x32 PNG image.

        Returns:
            The enum type for 32x32 PNG image.
        """
        return ImageType(_ImageTypeEnum.PNG32)

    @staticmethod
    def png64() -> Self:
        """Gets the enum type for 64x64 PNG image.

        Returns:
            The enum type for 64x64 PNG image.
        """
        return ImageType(_ImageTypeEnum.PNG64)

    @staticmethod
    def svg() -> Self:
        """Gets the enum type for SVG image.

        Returns:
            The enum type for SVG image.
        """
        return ImageType(_ImageTypeEnum.SVG)

    @classmethod
    def ascending_list(cls) -> list[Self]:
        return [ImageType(image_type) for image_type in _ImageTypeEnum]

    @staticmethod
    def get_image_type_from_path(image_path: Path) -> Self:
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
                return ImageType.png128()
            case "image-256.png":
                return ImageType.png256()
            case "image-32.png":
                return ImageType.png32()
            case "image-64.png":
                return ImageType.png64()
            case "image.svg":
                return ImageType.svg()
            case _:
                raise ValueError(f"Unknown image path: {image_path}")

    @staticmethod
    def get_png_image_type(size: int) -> Self:
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
                return ImageType.png128()
            case 256:
                return ImageType.png256()
            case 32:
                return ImageType.png32()
            case 64:
                return ImageType.png64()
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
        return base_dir.joinpath(self.file_name)
