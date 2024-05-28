from math import ceil

from bs4 import BeautifulSoup
from requests import get
from yarl import URL

from libraries.models.address import Address
from libraries.puller.getters.token_count_getter import TOKEN_COUNT_PER_PAGE
from libraries.puller.token_pullers.token_puller_abstracted import TokenPullerAbstracted

BLOCKSCOUT_API_URL: URL = URL("https://eth.blockscout.com/api/v2/tokens")
TOKEN_IMAGE_SELECTOR: str = (
    "#__next > div:nth-child(1) > div:nth-child(3) > div:nth-child(2) "
    + "> main > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > img"
)


class TokenPullerBlockscout(TokenPullerAbstracted):

    blockscout_url: URL
    token_image_map: dict[Address, URL] = {}

    def __init__(self, network):
        """Initialize the token puller blockscout class.

        Args:
            network: The network information.
        """
        super().__init__(network)
        self.blockscout_url = URL(
            str(
                next(filter(lambda x: x.id == "blockscout", self.network.explorers)).url
            )
        )

    def _get_top_token_list(self) -> set[tuple[int, Address]]:
        addresses = []
        page_param = {"items_count": TOKEN_COUNT_PER_PAGE}
        for _ in range(ceil(self.token_count / TOKEN_COUNT_PER_PAGE)):
            token_list, page_param = self.__get_token_list(page_param)
            addresses.extend(
                (idx, address)
                for idx, (address, _) in enumerate(token_list, len(addresses))
            )
            self.token_image_map.update({address: url for address, url in token_list})
        return set(addresses)

    def _get_token_url(self, address: Address) -> URL:
        return self.blockscout_url / "token" / address

    def _get_token_image_url(self, address: Address) -> URL | None:
        if address in self.token_image_map:
            return self.__find_larger_image_url(self.token_image_map[address])
        token_page = get(str(self._get_token_url(address)))
        if token_page.status_code != 200:
            return None
        soup = BeautifulSoup(token_page.content, "html.parser")
        if (img_url := soup.select_one(TOKEN_IMAGE_SELECTOR).get("src", None)) is None:
            return None
        return self.__find_larger_image_url(URL(img_url))

    def _download_token_image(self, token_image_url: URL) -> bytes | None:
        response = get(str(token_image_url))
        if response.status_code == 200:
            return response.content
        return None

    @staticmethod
    def __get_token_list(
        page_param: dict | None = None,
    ) -> tuple[list[tuple[Address, URL]], dict | None]:
        """Get the token list from the Blockscout explorer.

        Args:
            page_param: The page parameter. If None, the first page is used.

        Returns:
            The list of token address and token image URL, and the next page parameter.
        """
        page_param.update({"type": "ERC-20"})
        response = get(str(BLOCKSCOUT_API_URL), params=page_param)
        if response.status_code != 200:
            return [], None
        data: dict = response.json()
        data_list = list(
            filter(
                None,
                [
                    (
                        Address(item["address"]),
                        URL(item["icon_url"]).with_suffix(".png"),
                    )
                    for item in data.get("items", [])
                    if "address" in item and "icon_url" in item
                ],
            )
        )
        return data_list, data.get("next_page_params", None)

    @staticmethod
    def __find_larger_image_url(base_url: URL) -> URL | None:
        """Find a larger image URL.

        Args:
            base_url: The base URL.

        Returns:
            The larger image URL.
        """
        base_response = get(str(base_url))
        if base_response.status_code != 200:
            return None
        if "small" not in str(base_url):
            return base_url
        large_url = URL(str(base_url).replace("small", "large"))
        large_response = get(str(large_url))
        return large_url if large_response.status_code == 200 else base_url
