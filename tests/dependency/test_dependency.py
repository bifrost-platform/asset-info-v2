from os import listdir

from libraries.utils.dependency import read_requirements, read_essential_packages
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
    all_requirements = ["essential"] + list(extra_paths.keys())

    def test_requirements_files_exist(self):
        """Test the existence of the requirements files."""
        for key in self.all_requirements:
            assert PWD.joinpath(f"requirements/{key}.txt").exists()

    def test_unnecessary_requirements(self):
        """Test the unnecessary requirements in `requirements`."""
        for file in listdir(PWD.joinpath("requirements")):
            assert any(file.startswith(key) for key in self.all_requirements)

    def test_install_requires(self):
        """Test the `install_requires` in `setup.py`."""
        install_deps = [
            dep
            for deps in [
                get_dependencies(
                    PWD.joinpath(package.removesuffix("*").replace(".", "/"))
                )
                for package in read_essential_packages()
            ]
            for dep in deps
        ]
        install_requires = read_requirements("essential")
        for dep in set(install_deps):
            assert any(dep in require for require in install_requires)

    def test_extras_require(self):
        """Test the `extras_require` in `setup.py`."""
        for extra_key, extra_path in self.extra_paths.items():
            extra_requires = read_requirements(extra_key)
            assert extra_key in self.extra_paths
            extra_deps = get_dependencies(extra_path)
            for dep in extra_deps:
                assert any(dep in require for require in extra_requires)
