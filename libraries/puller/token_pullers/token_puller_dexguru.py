from math import ceil

from bs4 import BeautifulSoup
from requests import post, get
from yarl import URL

from libraries.models.address import Address
from libraries.models.engine import EngineEnum
from libraries.models.network import Network
from libraries.puller.getters.token_count_getter import TOKEN_COUNT_PER_PAGE
from libraries.puller.token_pullers.token_puller_abstracted import TokenPullerAbstracted

DEXGURU_GRAPHQL_URL: URL = URL("https://explorer-graph-prod.dexguru.biz/graphql")
TOKEN_IMAGE_SELECTOR: str = (
    "#page > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > img"
)


class TokenPullerDexguru(TokenPullerAbstracted):
    """Token puller using DexGuru explorer.

    Attributes:
        dexguru_url: The URL of the DexGuru explorer.
        token_image_map: The mapping of token address to token image URL.
    """

    dexguru_url: URL
    token_image_map: dict[Address, URL] = {}

    def __init__(self, network: Network) -> None:
        """Initialize the token puller dexguru class.

        Args:
            network: The network information.
        """
        super().__init__(network)
        self.dexguru_url = URL(
            str(next(filter(lambda x: x.id == "dexguru", self.network.explorers)).url)
        )

    def _get_top_token_list(self) -> set[tuple[int, Address]]:
        addresses = []
        for page in range(ceil(self.token_count / TOKEN_COUNT_PER_PAGE)):
            token_list = self.__get_token_list(page + 1)
            addresses.extend(
                (idx, address)
                for idx, (address, _) in enumerate(token_list, len(addresses))
            )
            self.token_image_map.update({address: url for address, url in token_list})
        return set(addresses)

    def _get_token_url(self, address: Address) -> URL:
        return self.dexguru_url / "token" / address.root

    def _get_token_image_url(self, address: Address) -> URL | None:
        if address in self.token_image_map:
            return self.token_image_map[address]
        token_page = get(str(self._get_token_url(address)))
        if token_page.status_code != 200:
            return None
        soup = BeautifulSoup(token_page.content, "html.parser")
        if (
            img_indirect_url := soup.select_one(TOKEN_IMAGE_SELECTOR).get("src", None)
        ) is None:
            return None
        if (img_url := URL(img_indirect_url).query.get("url", None)) is None:
            return None
        return URL(img_url)

    def _download_token_image(self, token_image_url: URL) -> bytes | None:
        response = get(str(token_image_url))
        if response.status_code == 200:
            return response.content
        return None

    def __get_token_list(self, page: int) -> list[tuple[Address, URL]]:
        """Get the token list from the DexGuru explorer.

        Args:
            page: The page number.

        Returns:
            The list of token address and token image URL.
        """
        payload = self.__create_token_list_payload(self.network, page)
        response = post(str(DEXGURU_GRAPHQL_URL), json=payload)
        if response.status_code != 200:
            return []
        data: dict = response.json()
        data_list = data.get("data", {}).get("topTokens", {}).get("data", [])
        return list(
            filter(
                None,
                [
                    (Address(data["address"]), URL(data["logoURI"]))
                    for data in data_list
                    if "address" in data and "logoURI" in data
                ],
            )
        )

    @staticmethod
    def __create_token_list_payload(network: Network, page: int) -> dict:
        """Create the payload for getting the token list.

        Args:
            network: The network information.
            page: The page number.

        Returns:
            The payload for getting the token list.

        Raises:
            AssertionError: If the network engine is not EVM.
        """
        assert network.engine == EngineEnum.EVM
        chain_id = network.id.split("-")[-1]
        return {
            "operationName": "TopTokens",
            "variables": {
                "first": TOKEN_COUNT_PER_PAGE,
                "skip": (page - 1) * TOKEN_COUNT_PER_PAGE,
                "onlyVerified": True,
            },
            "query": "query TopTokens($first: Long!, $skip: Long!, $onlyVerified: Boolean) { "
            + f"topTokens(first: $first, skip: $skip, onlyVerified: $onlyVerified, chainId: {chain_id}) {{ "
            + "data { address name symbol logoURI } total __typename } }",
        }
