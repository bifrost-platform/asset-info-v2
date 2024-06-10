from math import ceil

from bs4 import BeautifulSoup
from prompt_toolkit import print_formatted_text as printf, HTML
from requests import get
from web3 import Web3
from yarl import URL

from libraries.models.terminals.address import Address
from libraries.models.terminals.id import Id
from libraries.puller.getters.id_getter import get_id
from libraries.puller.getters.token_count_getter import TOKEN_COUNT_PER_PAGE
from libraries.puller.token_pullers.token_puller_abstracted import TokenPullerAbstracted

BLOCKSCOUT_TOKEN_ENDPOINT_PATH: str = "api/v2/tokens"
TOKEN_IMAGE_SELECTOR: str = "#__next > div > div > div > main > div > div > div > img"


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
        return self.blockscout_url / "token" / str(address)

    def _get_token_image_url(self, address: Address) -> URL | None:
        image_urls = self.__find_image_urls(address)
        if image_urls.count(None) >= 3:
            return next(filter(None, image_urls), None)
        else:
            base, small, large = image_urls
            available_images: dict[Id, URL] = dict()
            if large:
                available_images.update({Id("large"): large})
            if small:
                available_images.update({Id("small"): small})
            if base:
                available_images.update({Id("original"): base})
            printf(HTML(f"⎡ <b>Available images for {address}:</b>"))
            for size, url in available_images.items():
                printed_url = str(url).replace("&", "&amp;")
                printf(HTML(f"⎢ <b>∙ {size}</b>: {printed_url}"))
            selected_type = get_id(
                "⎣ Select the image type",
                None,
                set(available_images.keys()),
            )
            return available_images[selected_type]

    def _download_token_image(self, token_image_url: URL) -> bytes | None:
        response = get(str(token_image_url))
        if response.status_code == 200:
            return response.content
        return None

    def __get_token_list(
        self, page_param: dict | None = None
    ) -> tuple[list[tuple[Address, URL]], dict | None]:
        """Get the token list from the Blockscout explorer.

        Args:
            page_param: The page parameter. If None, the first page is used.

        Returns:
            The list of token address and token image URL, and the next page parameter.
        """
        page_param.update({"type": "ERC-20"})
        response = get(
            str(self.blockscout_url / BLOCKSCOUT_TOKEN_ENDPOINT_PATH), params=page_param
        )
        if response.status_code != 200:
            return [], None
        data: dict = response.json()
        data_list = list(
            filter(
                None,
                [
                    (
                        Address(Web3.to_checksum_address(item["address"])),
                        URL(item["icon_url"]).with_suffix(".png"),
                    )
                    for item in data.get("items", [])
                    if "address" in item and "icon_url" in item
                ],
            )
        )
        return data_list, data.get("next_page_params", None)

    def __find_image_urls(
        self, address: Address
    ) -> tuple[URL | None, URL | None, URL | None]:
        """Find the input token's small and large image URLs.

        Args:
            address: The address of the token.

        Returns:
            The base, small and large image URLs.
        """
        base_image_url = self.__find_base_image_url(address)
        if base_image_url is None:
            return None, None, None
        small_image_url = self.__find_small_image_url(base_image_url)
        large_image_url = self.__find_large_image_url(base_image_url)
        return (
            (
                base_image_url
                if base_image_url != small_image_url
                and base_image_url != large_image_url
                else None
            ),
            small_image_url,
            large_image_url,
        )

    def __find_base_image_url(self, address: Address) -> URL | None:
        """Find the input token's image URL.

        Args:
            address: The address of the token.

        Returns:
            The base image URL.
        """
        # Check if the token's image URL is already in the map.
        if address in self.token_image_map:
            response = get(str(self.token_image_map[address]))
            if response.status_code == 200:
                return self.token_image_map[address]
        # Get the token page.
        token_page = get(str(self._get_token_url(address)))
        if token_page.status_code != 200:
            return None
        # Parse the token page.
        soup = BeautifulSoup(token_page.content, "html.parser")
        if (img_soup := soup.select_one(TOKEN_IMAGE_SELECTOR)) is None:
            return None
        if (img_url := img_soup.get("src", None)) is None:
            return None
        return URL(img_url)

    @staticmethod
    def __find_small_image_url(base_url: URL) -> URL | None:
        """Find a smaller image URL.

        Args:
            base_url: The base URL.

        Returns:
            The smaller image URL.
        """
        str_base_url = str(base_url)
        if "small" in str_base_url:
            return base_url
        small_url = URL(str(base_url).replace("large", "small"))
        if small_url == base_url:
            return None
        small_response = get(str(small_url))
        return small_url if small_response.status_code == 200 else None

    @staticmethod
    def __find_large_image_url(base_url: URL) -> URL | None:
        """Find a larger image URL.

        Args:
            base_url: The base URL.

        Returns:
            The larger image URL.
        """
        str_base_url = str(base_url)
        if "large" in str_base_url:
            return base_url
        large_url = URL(str(base_url).replace("small", "large"))
        if large_url == base_url:
            return None
        large_response = get(str(large_url))
        return large_url if large_response.status_code == 200 else None
