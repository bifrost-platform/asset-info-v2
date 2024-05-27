from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
    prompt,
)
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError

from libraries.models.image_type import ImageTypeEnum


class ImageTypeValidator(Validator):
    """Validator for image type input.

    Attributes:
        permitted_image_types: The set of permitted image types.

    Args:
        permitted_image_types: The set of permitted image types to use for validation.
    """

    permitted_image_types: set[ImageTypeEnum]

    def __init__(self, permitted_image_types: set[ImageTypeEnum]) -> None:
        self.permitted_image_types = permitted_image_types

    def validate(self, document):
        """Validate the image type input."""
        text = document.text
        if text not in ImageTypeEnum.get_descending_type_list():
            raise ValidationError(message=f"Image type {text} not found")
        if text not in self.permitted_image_types:
            raise ValidationError(message=f"Image type {text} not permitted")


def get_image_type(
    msg: str, permitted_image_types: list[ImageTypeEnum] = None
) -> ImageTypeEnum:
    """Get the image type.

    Args:
        msg: The message to display.
        permitted_image_types: The set of permitted image types.

    Returns:
        The image type.
    """
    if permitted_image_types is None:
        permitted_image_types = set(ImageTypeEnum.get_descending_type_list())
    printf(HTML(f"<b>{msg}: </b>" + ", ".join(permitted_image_types)))
    image_type_completer = WordCompleter(permitted_image_types)
    image_type = prompt(
        HTML("<b>> </b>"),
        completer=image_type_completer,
        placeholder=permitted_image_types[0],
        validator=ImageTypeValidator(set(permitted_image_types)),
    )
    return ImageTypeEnum(image_type)
