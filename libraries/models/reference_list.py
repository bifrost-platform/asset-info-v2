from json import loads
from pathlib import Path
from typing import Self

from libraries.models.reference import Reference
from libraries.models.templates.list_model import ListModel


class ReferenceList(ListModel[Reference]):
    """A constrained `list` of `Reference`."""

    def validate_items(self) -> Self:
        for idx in range(len(self.root) - 1):
            fst = self.root[idx]
            snd = self.root[idx + 1]
            if fst.id >= snd.id:
                raise ValueError(
                    "Reference list must be sorted by ID in ascending order and unique, but got "
                    + f"""{fst.id}, before {snd.id}"""
                )
        return self

    @staticmethod
    def get_ref_list(file_path: Path) -> Self:
        """Gets the reference list from the given file path.

        Args:
            file_path: The file path of the reference list.

        Returns:
            The reference list.
        """
        with open(file_path, "r") as fp:
            return ReferenceList.model_validate(loads(fp.read()))
