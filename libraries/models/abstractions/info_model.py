from abc import ABCMeta
from json import loads
from pathlib import Path
from typing import Self

from libraries.models.terminals.id import Id
from libraries.models.image_info import ImageInfo
from libraries.models.terminals.info_category import InfoCategory
from libraries.models.terminals.tag_list import TagList
from libraries.models.templates.camelcase_model import CamelCaseModel
from libraries.utils.file import search


class InfoModel(CamelCaseModel, metaclass=ABCMeta):
    """The base model of information about each blockchain network.

    Attributes:
        id: ID of the asset (`Id`: constrained `str`.)
        images: information about the existence of each image type (`ImageInfo`)
        name: name of the asset (`str`: must be the same as one of the contract's names.)
        tags: tags of the asset (`TagList`: constrained `list` of `Tag`.)
    """

    id: Id
    images: ImageInfo
    name: str
    tags: TagList

    @staticmethod
    def get_info_category() -> InfoCategory:
        """Gets the information category.

        Returns:
            The information category.
        """
        raise NotImplementedError

    @classmethod
    def __read_info(cls, file_path: Path) -> tuple[Self, Path]:
        """Reads the information from the file.

        Args:
            file_path: the path of the file.

        Returns:
            The information.
        """
        with open(file_path, "r") as fp:
            return cls.model_validate(loads(fp.read())), file_path

    @classmethod
    def get_info_list(cls) -> list[tuple[Self, Path]]:
        """Gets the list of information.

        Returns:
            The list of information.
        """
        info_category = cls.get_info_category()
        return [
            cls.__read_info(file_path)
            for file_path in search(info_category.get_model_dir_path(), r"^info\.json$")
        ]
