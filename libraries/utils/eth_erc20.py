from decimal import Decimal

from pydantic import HttpUrl
from web3 import Web3, HTTPProvider
from web3.contract import Contract
from web3.exceptions import BadFunctionCallOutput

from libraries.utils.file import PWD


class EthErc20Interface:
    """Interface for ERC20 tokens on Ethereum network.

    Attributes:
        node: The Web3 interface connected with input node.
        contract: The ERC20 contract.

    Args:
        node_url: The node URL.
        address: The contract address.
    """

    node: Web3
    contract: Contract

    def __init__(self, node_url: HttpUrl, address: str):
        self.node = Web3(HTTPProvider(node_url))
        assert self.node.is_connected()
        with open(PWD.joinpath("libraries/constants/erc20.abi.json")) as fp:
            self.contract = self.node.eth.contract(
                self.node.to_checksum_address(address), abi=fp.read()
            )

    def get_name(self) -> str:
        """Get the name of the token.

        Returns:
            The name of the token.
        """
        method = self.contract.functions.name()
        try:
            return method.call()
        except BadFunctionCallOutput:
            result = self.node.eth.call(method.build_transaction())
            return result.decode("utf-8").replace("\x00", "")

    def get_symbol(self) -> str:
        """Get the symbol of the token.

        Returns:
            The symbol of the token.
        """
        method = self.contract.functions.symbol()
        try:
            return method.call()
        except BadFunctionCallOutput:
            result = self.node.eth.call(method.build_transaction())
            return result.decode("utf-8").replace("\x00", "")

    def get_decimals(self) -> int:
        """Get the decimals of the token.

        Returns:
            The decimals of the token.
        """
        return self.contract.functions.decimals().call()

    def get_total_supply_raw(self) -> int:
        """Get the current total supply of the token in raw format.

        Returns:
            The raw format of the token's current total supply.
        """
        return self.contract.functions.totalSupply().call()

    def get_total_supply(self) -> Decimal:
        """Get the current total supply of the token.

        Returns:
            The total supply of the token's current total supply.
        """
        return self.__convert_raw_to_decimal(self.get_total_supply_raw())

    def get_balance_raw(self, address: str) -> int:
        """Get the current token balance of the account in raw format.

        Args:
            address: The address of account to check the balance.

        Returns:
            The raw format of the account's current token balance.
        """
        return self.contract.functions.balanceOf(address).call()

    def get_balance(self, address: str) -> Decimal:
        """Get the current token balance of the account.

        Args:
            address: The address of account to check the balance.

        Returns:
            The account's current token balance.
        """
        return self.__convert_raw_to_decimal(self.get_balance_raw(address))

    def get_allowance_raw(self, owner: str, spender: str) -> int:
        """Get the current allowance of the owner to the spender in raw format.

        Args:
            owner: The owner's address.
            spender: The spender's address.

        Returns:
            The raw format of the owner's allowance to the spender.
        """
        return self.contract.functions.allowance(owner, spender).call()

    def get_allowance(self, owner: str, spender: str) -> Decimal:
        """Get the current allowance of the owner to the spender.

        Args:
            owner: The owner's address.
            spender: The spender's address.

        Returns:
            The owner's allowance to the spender.
        """
        return self.__convert_raw_to_decimal(self.get_allowance_raw(owner, spender))

    def __convert_raw_to_decimal(self, raw: int) -> Decimal:
        """Convert the raw format to the decimal format.

        Args:
            raw: The raw format to convert.

        Returns:
            The decimal format of the input raw format.
        """
        return Decimal(raw) / Decimal(10 ** self.get_decimals())
