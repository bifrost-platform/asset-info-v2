from bs4 import BeautifulSoup
from prompt_toolkit import print_formatted_text as printf, HTML
from requests import get
from web3 import Web3
from yarl import URL

from libraries.models.network import Network
from libraries.models.terminals.address import Address
from libraries.models.terminals.id import Id
from libraries.preprocess.image import PNG_TYPES
from libraries.puller.getters.id_getter import get_id
from libraries.puller.getters.token_count_getter import TOKEN_COUNT_PER_PAGE
from libraries.puller.token_pullers.token_puller_abstracted import TokenPullerAbstracted

ROUTESCAN_API_URL: URL = URL("https://api.routescan.io/")
TOKEN_IMAGE_SELECTOR: str = "#token > div > div > div > div > div > span > img"


class TokenPullerRoutescan(TokenPullerAbstracted):
    """Token puller using Routescan explorer.

    Attributes:
        routescan_url: The URL of the Routescan explorer.
    """

    routescan_url: URL

    def __init__(self, network: Network) -> None:
        """Initialize the token puller routescan class.

        Args:
            network: The network information.
        """
        super().__init__(network)
        self.routescan_url = URL(
            str(next(filter(lambda x: x.id == "routescan", self.network.explorers)).url)
        )

    def _get_top_token_list(self) -> set[tuple[int, Address]]:
        addresses = []
        path = (
            URL("/v2/network/mainnet/")
            / str(self.network.id).replace("-", "/")
            / "erc20"
        )
        while len(addresses) < self.token_count:
            token_list, path = self.__get_token_list(path)
            addresses.extend(
                [
                    (idx, address)
                    for idx, address in enumerate(token_list, len(addresses))
                ]
            )
        return addresses

    def _get_token_url(self, address: Address) -> URL:
        return self.routescan_url / "token" / str(address)

    def _get_token_image_url(self, address: Address) -> URL | None:
        # Get the token page for getting the token image URL.
        token_page = get(str(self._get_token_url(address)))
        if token_page.status_code != 200:
            return None
        soup = BeautifulSoup(token_page.content, "html.parser")
        if (image_soup := soup.select_one(TOKEN_IMAGE_SELECTOR)) is None:
            return None
        if (image_src := image_soup.get("src", None)) is None:
            return None
        base_url = URL(image_src)
        available_images: dict[Id, str] = dict()
        for size in PNG_TYPES:
            url = base_url.update_query([("w", size.size)])
            response = get(url)
            if response.status_code == 200 and response.url == str(url):
                available_images.update({Id(str(size).lower()): url})
        if base_url not in available_images.values():
            available_images.update({Id("original"): base_url})
        # Select the image type.
        if len(available_images) == 1:
            return next(iter(available_images.values()))
        else:
            printf(HTML(f"⎡ <b>Available images for {address}:</b>"))
            for size, url in available_images.items():
                printed_url = str(url).replace("&", "&amp;")
                printf(HTML(f"⎢ <b>∙ {size}</b>: {printed_url}"))
            selected_type = get_id(
                "⎣ Select the image type",
                permitted_id=set(available_images.keys()),
            )
            return URL(available_images[selected_type])

    def _download_token_image(self, token_image_url: URL) -> bytes | None:
        response = get(str(token_image_url))
        if response.status_code == 200:
            return response.content
        return None

    @staticmethod
    def __get_token_list(sub_path: URL) -> tuple[list[Address], URL | None]:
        """Get the list of tokens from the Routescan explorer.

        Args:
            sub_path: The sub-path of the Routescan API URL.

        Returns:
            A tuple containing the list of token addresses and the next sub-path.
        """
        response = get(
            str(ROUTESCAN_API_URL.join(sub_path)),
            params={"sort": "marketCap,desc", "limit": TOKEN_COUNT_PER_PAGE},
        )
        if response.status_code != 200:
            return []
        else:
            body: dict = response.json()
            next_sub_path = body.get("link", {}).get("next", None)
            return (
                [
                    Address(Web3.to_checksum_address(item["address"]))
                    for item in body.get("items", [])
                ],
                URL(next_sub_path) if next_sub_path is not None else None,
            )
