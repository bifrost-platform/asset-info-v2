from os import listdir

from libraries.utils.dependency import (
    packages,
    install_require_key,
    read_requirements,
    extras_require_keys,
)
from libraries.utils.file import PWD
from tests.utils.dependency_getter import get_dependencies


class TestDependencyOnSetupPy:
    """Tests the dependency on `setup.py`.

    Attributes:
        extra_paths: The paths for testing each extra requirement.
    """

    extra_paths = {
        "all": PWD,
        "dev": PWD.joinpath("libraries"),
        "test": PWD.joinpath("tests"),
    }

    def test_requirements_files_exist(self):
        """Test the existence of the requirements files."""
        for key in [install_require_key] + extras_require_keys:
            assert PWD.joinpath(f"requirements/{key}.txt").exists()

    def test_unnecessary_requirements(self):
        """Test the unnecessary requirements in `requirements`."""
        for file in listdir(PWD.joinpath("requirements")):
            assert any(
                file.startswith(key)
                for key in [install_require_key] + extras_require_keys
            )

    def test_install_requires(self):
        """Test the `install_requires` in `setup.py`."""
        install_deps = [
            dep
            for deps in [
                get_dependencies(PWD.joinpath(package.replace(".", "/")))
                for package in packages
            ]
            for dep in deps
        ]
        install_requires = read_requirements(install_require_key)
        for dep in install_deps:
            assert any(dep in require for require in install_requires)

    def test_extras_require(self):
        """Test the `extras_require` in `setup.py`."""
        for extra_key in extras_require_keys:
            extra_requires = read_requirements(extra_key)
            assert extra_key in self.extra_paths
            extra_deps = get_dependencies(self.extra_paths[extra_key])
            for dep in extra_deps:
                assert any(dep in require for require in extra_requires)
