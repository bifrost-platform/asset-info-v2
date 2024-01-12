from libraries.utils.model import CamelCaseModel


class ImageInfo(CamelCaseModel):
    """The base model of information about the existence of each image type.

    Attributes:
        png128: whether the image in PNG format with 128x128 pixels exists. (:class:`bool`)
        png256: whether the image in PNG format with 256x256 pixels exists. (:class:`bool`)
        png32: whether the image in PNG format with 32x32 pixels exists. (:class:`bool`)
        png64: whether the image in PNG format with 64x64 pixels exists. (:class:`bool`)
        svg: whether the image in SVG format exists. (:class:`bool`)
    """

    png128: bool
    png256: bool
    png32: bool
    png64: bool
    svg: bool
