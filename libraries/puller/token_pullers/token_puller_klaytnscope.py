from base64 import decode
from io import BytesIO
from math import ceil

from requests import get
from web3 import Web3
from yarl import URL

from libraries.models.network import Network
from libraries.models.terminals.address import Address
from libraries.puller.token_pullers.token_puller_abstracted import TokenPullerAbstracted

ALLBIT_API_URL: URL = URL("https://api.allbit.com/token/v1/klaytn/scope/tokens")
KLAYTNSCOPE_API_URL: URL = URL("https://api-cypress.klaytnscope.com/v2/tokens")
TOKEN_COUNT_PER_PAGE: int = 25


class TokenPullerKlaytnscope(TokenPullerAbstracted):
    """Token puller using KlaytnScope explorer.

    Attributes:
        klaytnscope_url: The URL of the KlaytnScope explorer.
    """

    klaytnscope_url: URL
    token_image_map: dict[Address, URL] = {}

    def __init__(self, network: Network) -> None:
        """Initialize the token puller klaytnscope class.

        Args:
            network: The network information.
        """
        super().__init__(network)
        self.klaytnscope_url = URL(
            str(
                next(
                    filter(lambda x: x.id == "klaytnscope", self.network.explorers)
                ).url
            )
        )

    def _get_top_token_list(self) -> set[tuple[int, Address]]:
        addresses = list()
        for page in range(ceil(self.token_count / TOKEN_COUNT_PER_PAGE)):
            # Get the token list from the KlaytnScope explorer.
            token_list = self.__get_token_list(page + 1)
            for idx, (address, url) in enumerate(token_list, len(addresses)):
                # Collect the token image URL.
                addresses.append((idx, address))
                # Update the token image cache map collected from the token list.
                self.token_image_map.update({address: url})
        return set(addresses)

    def _get_token_url(self, address: Address) -> URL:
        return self.klaytnscope_url / "token" / str(address)

    def _get_token_image_url(self, address: Address) -> URL | None:
        # Check if the token's image URL is already cached.
        if address in self.token_image_map:
            response = get(str(self.token_image_map[address]))
            if response.status_code == 200:
                return self.token_image_map[address]
        # Get the token image URL.
        return self.__get_token_base64_image(address)

    def _download_token_image(self, token_image_url: URL) -> bytes | None:
        # Check if the token image URL is a base64 image.
        if "data" in token_image_url.scheme:
            output = BytesIO()
            decode(BytesIO(token_image_url.path.split(",")[-1].encode("ascii")), output)
            return output.getvalue()
        else:
            response = get(str(token_image_url))
            if response.status_code == 200:
                return response.content
            else:
                return None

    @staticmethod
    def __get_token_list(page: int) -> list[tuple[Address, URL]]:
        """Get the token list from the KlaytnScope explorer.

        Args:
            page: The page number of the token list.

        Returns:
            The token list.
        """
        response = get(str(ALLBIT_API_URL), params={"page": page})
        if response.status_code != 200:
            return []
        data: dict = response.json()
        data_list = [
            (Address(Web3.to_checksum_address(item["address"])), URL(item["icon"]))
            for item in data.get("data", [])
            if "address" in item and "icon" in item
        ]
        return list(filter(None, data_list))

    @staticmethod
    def __get_token_base64_image(address: Address) -> URL | None:
        """Get the token's base64 image URL.

        Args:
            address: The token address.

        Returns:
            The token's base64 image URL.
        """
        response = get(str(KLAYTNSCOPE_API_URL / address))
        if response.status_code != 200:
            return None
        data: dict = response.json()
        base64_image = data.get("result", {}).get("image", None)
        if base64_image is None:
            return None
        return URL(f"data:image/png;base64,{base64_image}")
