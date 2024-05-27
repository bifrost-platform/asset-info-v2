from math import ceil
from re import sub

from bs4 import BeautifulSoup
from requests import get
from yarl import URL

from libraries.models.address import Address
from libraries.models.network import Network
from libraries.preprocess.image import PNG_SIZES
from libraries.puller.getters.token_count_getter import TOKEN_COUNT_PER_PAGE
from libraries.puller.token_pullers.token_puller_abstracted import TokenPullerAbstracted

HEADER: dict[str, str] = {"User-Agent": "Mozilla/5.0"}
TOKEN_ADDRESS_SELECTOR: str = (
    "#ContentPlaceHolder1_tblErc20Tokens > table > tbody > tr > td > a"
)
TOKEN_IMAGE_SELECTOR: str = "#content > section > div > div > img"


class TokenPullerEtherscan(TokenPullerAbstracted):
    """Token puller using Etherscan explorer.

    Attributes:
        etherscan_url: The URL of the Etherscan explorer.
    """

    etherscan_url: URL

    def __init__(self, network: Network) -> None:
        """Initialize the token puller etherscan class.

        Args:
            network: The network information.
        """
        super().__init__(network)
        self.etherscan_url = URL(
            str(next(filter(lambda x: x.id == "etherscan", self.network.explorers)).url)
        )

    def _get_top_token_list(self) -> set[Address]:
        addresses = []
        for page in range(ceil(self.token_count / TOKEN_COUNT_PER_PAGE)):
            token_list_page = get(
                str(self.__get_token_list_url(page + 1)), headers=HEADER
            )
            if token_list_page.status_code != 200:
                break
            soup = BeautifulSoup(token_list_page.content, "html.parser")
            items = soup.select(TOKEN_ADDRESS_SELECTOR)
            addresses.extend(Address(item.get("href").split("/")[-1]) for item in items)
        return set(addresses)

    def _get_token_url(self, address: Address) -> URL:
        return self.etherscan_url / "token" / address

    def _get_token_image_url(self, address: Address) -> URL | None:
        token_page = get(str(self._get_token_url(address)), headers=HEADER)
        if token_page.status_code != 200:
            return None
        soup = BeautifulSoup(token_page.content, "html.parser")
        if (prefix := soup.select_one(TOKEN_IMAGE_SELECTOR).get("src", None)) is None:
            return None
        base_url = (self.etherscan_url / prefix.lstrip("/")).with_suffix(".png")
        for size in PNG_SIZES:
            url = sub(r"(_\d+)?.png", f"_{size}.png", str(base_url))
            response = get(url, headers=HEADER)
            if response.status_code == 200 and response.url == url:
                return URL(url)
        return base_url

    def _download_token_image(self, token_image_url: URL) -> bytes | None:
        response = get(str(token_image_url), headers=HEADER)
        if response.status_code == 200:
            return response.content
        return None

    def __get_token_list_url(self, page: int) -> URL:
        """Get the URL of the token list.

        Returns:
            The URL of the token list.
        """
        return self.etherscan_url / "tokens" % {"p": page, "ps": TOKEN_COUNT_PER_PAGE}
