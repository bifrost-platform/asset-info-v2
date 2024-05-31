from typing import Iterator, Self

from libraries.models.image_type import ImageType
from libraries.models.templates.camelcase_model import CamelCaseModel


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
    def create_empty() -> Self:
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

    def get(self, image_type: ImageType) -> bool:
        """Get the flag of image type.

        Args:
            image_type: The image type to get.

        Returns:
            The flag of image type.
        """
        if image_type.is_png128:
            return self.png128
        elif image_type.is_png256:
            return self.png256
        elif image_type.is_png32:
            return self.png32
        elif image_type.is_png64:
            return self.png64
        elif image_type.is_svg:
            return self.svg
        else:
            raise ValueError(f"Unknown image type: {image_type}")

    def set(self, image_type: ImageType):
        """Set the flag of image type.

        Args:
            image_type: The image type to set.
        """
        if image_type.is_png128:
            self.png128 = True
        elif image_type.is_png256:
            self.png256 = True
        elif image_type.is_png32:
            self.png32 = True
        elif image_type.is_png64:
            self.png64 = True
        elif image_type.is_svg:
            self.svg = True
        else:
            raise ValueError(f"Unknown image type: {image_type}")

    def unset(self, image_type: ImageType):
        """Unset the flag of image type.

        Args:
            image_type: The image type to unset.
        """
        if image_type.is_png128:
            self.png128 = False
        elif image_type.is_png256:
            self.png256 = False
        elif image_type.is_png32:
            self.png32 = False
        elif image_type.is_png64:
            self.png64 = False
        elif image_type.is_svg:
            self.svg = False

    def __iter__(self) -> Iterator[tuple[ImageType, bool]]:
        """Iterate the image type and flag.

        Returns:
            The iterator of image type and flag.

        Notes:
            The image types are iterated in ascending order.
        """
        return iter(
            [
                (image_type, self.get(image_type))
                for image_type in ImageType.ascending_list()
            ]
        )
