from typing import Iterator

from libraries.models.image_type import ImageTypeEnum
from libraries.utils.model import CamelCaseModel


class ImageInfo(CamelCaseModel):
    """The base model of information about the existence of each image type.

    Attributes:
        png128: whether the image in PNG format with 128x128 pixels exists.
        png256: whether the image in PNG format with 256x256 pixels exists.
        png32: whether the image in PNG format with 32x32 pixels exists.
        png64: whether the image in PNG format with 64x64 pixels exists.
        svg: whether the image in SVG format exists.
    """

    png128: bool
    png256: bool
    png32: bool
    png64: bool
    svg: bool

    @staticmethod
    def create_empty() -> "ImageInfo":
        """Create empty image information.

        Returns:
            The empty image information.
        """
        return ImageInfo(
            png128=False,
            png256=False,
            png32=False,
            png64=False,
            svg=False,
        )

    def get(self, image_type: ImageTypeEnum) -> bool:
        """Get the flag of image type.

        Args:
            image_type: The image type to get.

        Returns:
            The flag of image type.
        """
        match image_type:
            case ImageTypeEnum.PNG128:
                return self.png128
            case ImageTypeEnum.PNG256:
                return self.png256
            case ImageTypeEnum.PNG32:
                return self.png32
            case ImageTypeEnum.PNG64:
                return self.png64
            case ImageTypeEnum.SVG:
                return self.svg

    def set(self, image_type: ImageTypeEnum):
        """Set the flag of image type.

        Args:
            image_type: The image type to set.
        """
        match image_type:
            case ImageTypeEnum.PNG128:
                self.png128 = True
            case ImageTypeEnum.PNG256:
                self.png256 = True
            case ImageTypeEnum.PNG32:
                self.png32 = True
            case ImageTypeEnum.PNG64:
                self.png64 = True
            case ImageTypeEnum.SVG:
                self.svg = True

    def unset(self, image_type: ImageTypeEnum):
        """Unset the flag of image type.

        Args:
            image_type: The image type to unset.
        """
        match image_type:
            case ImageTypeEnum.PNG128:
                self.png128 = False
            case ImageTypeEnum.PNG256:
                self.png256 = False
            case ImageTypeEnum.PNG32:
                self.png32 = False
            case ImageTypeEnum.PNG64:
                self.png64 = False
            case ImageTypeEnum.SVG:
                self.svg = False

    def __iter__(self) -> Iterator[tuple[ImageTypeEnum, bool]]:
        """Iterate the image type and flag.

        Returns:
            The iterator of image type and flag.

        Notes:
            The image types are iterated in ascending order.
        """
        return iter(
            [
                (image_type, self.get(image_type))
                for image_type in ImageTypeEnum.get_ascending_type_list()
            ]
        )
