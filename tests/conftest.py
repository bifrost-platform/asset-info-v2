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
    parser.addoption(
        "--all",
        action="store_true",
        help="Run all tests.",
    )


def pytest_configure(config: pytest.Config):
    config.addinivalue_line("markers", "rpc: Skip the RPC connection using test.")
    config.addinivalue_line("markers", "image: Skip the image test.")
    config.addinivalue_line("markers", "all: Run all tests.")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]):
    if config.getoption("--all", default=False):
        return
    else:
        skip_not_all = pytest.mark.skip(reason="Skip the test in all.")
        skip_rpc = pytest.mark.skip(reason="Skip the RPC connection using test.")
        skip_image = pytest.mark.skip(reason="Skip the image test.")
        for item in items:
            if "all" in item.keywords:
                item.add_marker(skip_not_all)
            elif config.getoption("--skip-rpc-using-test") and "rpc" in item.keywords:
                item.add_marker(skip_rpc)
            elif config.getoption("--skip-image-test") and "image" in item.keywords:
                item.add_marker(skip_image)
