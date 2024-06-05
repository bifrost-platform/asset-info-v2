import pytest


def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--skip-rpc-using-test",
        action="store_true",
        help="Skip the RPC connection using test.",
    )
    parser.addoption(
        "--skip-image-test", action="store_true", help="Skip the image test."
    )


def pytest_configure(config: pytest.Config):
    config.addinivalue_line("markers", "rpc: Skip the RPC connection using test.")
    config.addinivalue_line("markers", "image: Skip the image test.")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]):
    if config.getoption("--skip-rpc-using-test"):
        skip_rpc = pytest.mark.skip(reason="Skip the RPC connection using test.")
        for item in items:
            if "rpc" in item.keywords:
                item.add_marker(skip_rpc)
    if config.getoption("--skip-image-test"):
        skip_image = pytest.mark.skip(reason="Skip the image test.")
        for item in items:
            if "image" in item.keywords:
                item.add_marker(skip_image)
