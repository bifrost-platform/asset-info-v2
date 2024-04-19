import io
from pathlib import Path

from pigar.core import RequirementsAnalyzer
from pigar.parser import DEFAULT_GLOB_EXCLUDE_PATTERNS


def get_dependencies(path: Path) -> list[str]:
    """Gets the dependencies of the given directory.

    Args:
        path: The path of the directory.

    Returns:
        The list of packages that the directory depends on.
    """
    analyzer = RequirementsAnalyzer(str(path))
    buf = io.StringIO()
    comparison_specifier = "=="
    analyzer.analyze_requirements(
        visit_doc_str=False,
        follow_symbolic_links=False,
        ignores=DEFAULT_GLOB_EXCLUDE_PATTERNS,
    )
    analyzer.write_requirements(
        buf,
        with_ref_comments=False,
        with_banner=False,
        with_unknown_imports=False,
        comparison_specifier=comparison_specifier,
    )
    return [
        dep.split(comparison_specifier)[0]
        for dep in filter(
            lambda x: comparison_specifier in x, buf.getvalue().split("\n")
        )
    ]
