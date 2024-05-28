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
        allow_none: Whether to allow None as an image type.
        permitted_image_types: The set of permitted image types.

    Args:
        allow_none: Whether to allow None as an image type.
        permitted_image_types: The set of permitted image types to use for validation.
    """

    allow_none: bool
    permitted_image_types: set[ImageTypeEnum]

    def __init__(
        self, allow_none: bool, permitted_image_types: set[ImageTypeEnum]
    ) -> None:
        self.allow_none = allow_none
        self.permitted_image_types = permitted_image_types

    def validate(self, document):
        """Validate the image type input."""
        text = document.text
        if not text and self.allow_none:
            return
        if text not in ImageTypeEnum.get_descending_type_list():
            raise ValidationError(message=f"Image type {text} not found")
        if text not in self.permitted_image_types:
            raise ValidationError(message=f"Image type {text} not permitted")


def get_image_type(
    msg: str,
    permitted_image_types: list[ImageTypeEnum] = None,
    allow_none: bool = False,
) -> ImageTypeEnum | None:
    """Get the image type.

    Args:
        msg: The message to display.
        permitted_image_types: The set of permitted image types.
        allow_none: Whether to allow None as an image type.

    Returns:
        The image type.
    """
    if permitted_image_types is None:
        permitted_image_types = set(ImageTypeEnum.get_descending_type_list())
    printf(
        HTML(
            f"<b>{msg}: </b>"
            + ", ".join(permitted_image_types)
            + (", <grey>blank</grey> (for Original)" if allow_none else "")
        )
    )
    image_type_completer = WordCompleter(
        permitted_image_types + ([""] if allow_none else [])
    )
    image_type = prompt(
        HTML("<b>> </b>"),
        completer=image_type_completer,
        placeholder=None if allow_none else permitted_image_types[0],
        validator=ImageTypeValidator(allow_none, set(permitted_image_types)),
    )
    return ImageTypeEnum(image_type) if image_type else None
