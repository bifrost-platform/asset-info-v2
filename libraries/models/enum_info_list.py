from json import loads
from typing import Self

from libraries.models.abstractions.enum_type_model import EnumTypeModel
from libraries.models.enum_info import EnumInfo
from libraries.models.templates.list_model import ListModel


class EnumInfoList(ListModel[EnumInfo]):
    """A constrained `list` of `EnumInfo`."""

    def validate_items(self) -> Self:
        for idx in range(len(self.root) - 1):
            fst, snd = idx, idx + 1
            if self.root[fst].value >= self.root[snd].value:
                raise ValueError(
                    "Enum info list must be sorted by value in ascending order and unique, but got "
                    + f"""'{self.root[fst].value}', before '{self.root[snd].value}'"""
                )
        return self

    @staticmethod
    def get_info_list(enum_type: EnumTypeModel) -> Self:
        """Gets the enum information list from the given enum type.

        Args:
            enum_type: The enum type model.

        Returns:
            The enum information list.
        """
        with open(enum_type.get_enum_path(), "r") as fp:
            return EnumInfoList.model_validate(loads(fp.read()))
