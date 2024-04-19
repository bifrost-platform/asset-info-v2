from setuptools import setup

install_required = ["pydantic==2.5.3"]

dev_required = [
    "CairoSVG==2.7.1",
    "pillow==10.2.0",
    "pytest==7.4.4",
    "svgpathtools==1.6.1",
    "web3==6.14.0",
]

setup(
    name="asset-info-v2",
    version="1.0.0",
    packages=[
        "libraries.utils",
        "libraries.models",
    ],
    install_requires=install_required,
    extras_require={"dev": dev_required},
    url="https://github.com/bifrost-platform/asset-info-v2",
    license="",
    author="Backend Team of Bifrost",
    author_email="contact@pi-lab.io",
    description="Information about asset ver.2",
)
