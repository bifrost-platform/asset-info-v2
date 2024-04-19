from setuptools import setup

from libraries.utils.dependency import (
    packages,
    read_requirements,
    install_require_key,
    extras_require_keys,
)

install_requires = read_requirements(install_require_key)
extras_require = {key: read_requirements(key) for key in extras_require_keys}

setup(
    name="asset-info-v2",
    version="1.0.0",
    packages=packages,
    install_requires=install_requires,
    extras_require=extras_require,
    url="https://github.com/bifrost-platform/asset-info-v2",
    license="",
    author="Backend Team of Bifrost",
    author_email="contact@pi-lab.io",
    description="Information about asset ver.2",
)
