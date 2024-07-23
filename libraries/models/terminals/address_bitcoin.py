from typing import Self

from bitcoinlib.encoding import EncodingError
from bitcoinlib.keys import deserialize_address

from libraries.models.templates.str_model import StrModel


class AddressBitcoin(StrModel):
    """A constrained `str` for the Bitcoin address."""

    @property
    def __deserialized_result(self) -> dict:
        """The result from the deserialization the Bitcoin address."""
        return deserialize_address(self.root)

    @property
    def public_key_hash(self) -> str:
        """The public key hash of the Bitcoin address."""
        return self.__deserialized_result.get("public_key_hash")

    @property
    def encoding_type(self) -> str:
        """The encoding type of the Bitcoin address."""
        return self.__deserialized_result.get("encoding")

    @property
    def script_type(self) -> str:
        """The script type of the Bitcoin address."""
        return self.__deserialized_result.get("script_type")

    def __eq__(self, other: Self | str) -> bool:
        match other:
            case AddressBitcoin():
                return self.root.lower() == other.root.lower()
            case str():
                return self.root.lower() == other.lower()
            case _:
                raise ValueError(f"Cannot compare {self} with {other}")

    def __lt__(self, other: Self) -> bool:
        return self.public_key_hash < other.public_key_hash

    def __hash__(self) -> int:
        return hash(self.public_key_hash)

    def validate_str(self) -> Self:
        try:
            return deserialize_address(self.root).get("address")
        except EncodingError:
            raise ValueError(f"Invalid Bitcoin address: {self.root}")
