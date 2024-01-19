from setuptools import setup

with open("requirements.txt") as f:
    required = [require.replace("==", ">=") for require in f.read().splitlines()]

setup(
    name="asset-info-v2",
    version="1.0.0",
    packages=[
        "libraries.utils",
        "libraries.models",
    ],
    install_requires=required,
    url="https://github.com/bifrost-platform/asset-info-v2",
    license="",
    author="Backend Team of Bifrost",
    author_email="contact@pi-lab.io",
    description="Information about asset ver.2  ",
)
