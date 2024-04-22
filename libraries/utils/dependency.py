from re import search

REQUIREMENT_REFERENCE_REGEX = r"^\-r ([\w]+)\.txt$"


def read_requirements(key: str) -> list[str]:
    """Reads the requirements from the given type.

    Args:
        key: The key of the requirements.

    Returns:
        The list of requirements.
    """
    with open(f"requirements/{key}.txt") as file:
        req_lines = list(
            filter(
                lambda x: not x.startswith("#"),
                file.read().splitlines(),
            )
        )
    ref_keys = [
        search(REQUIREMENT_REFERENCE_REGEX, req).group(1)
        for req in filter(lambda x: x.startswith("-r"), req_lines)
    ]
    ref_reqs = [
        req
        for reqs in [read_requirements(ref_type) for ref_type in ref_keys]
        for req in reqs
    ]
    reqs = list(filter(lambda x: not x.startswith("-r"), req_lines))
    return ref_reqs + reqs


packages = ["libraries.models"]
"""List of packages to be used by the users."""

install_require_key = "essential"
"""The key of the essential requirements."""

extras_require_keys = ["all", "dev", "test"]
"""The keys of the extra requirements."""
