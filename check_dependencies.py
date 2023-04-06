#!/usr/bin/env python

import sys
from importlib.metadata import PackageNotFoundError, version

REQUIRED_DEPENDENCIES = ["biopython>=1.43"]

REQUIRED_PYTHON_VERSION = ">=3.7"

SPECIFIERS = [
    (">=", lambda v1, v2: v1 >= v2),
    ("<=", lambda v1, v2: v1 <= v2),
    (">", lambda v1, v2: v1 > v2),
    ("<", lambda v1, v2: v1 < v2),
    ("==", lambda v1, v2: v1 == v2),
    ("!=", lambda v1, v2: v1 != v2),
]


def parse_version_string(version_string):
    return tuple(map(int, version_string.split(".")))


def parse_requirement(requirement_string):
    for specifier, comparator in SPECIFIERS:
        if specifier in requirement_string:
            package_name, version_string = requirement_string.split(specifier)
            min_version = parse_version_string(version_string.strip())
            return package_name, comparator, min_version
    return requirement_string, None, None


def check_python_version():
    current_python_version = parse_version_string(
        ".".join(map(str, sys.version_info[:3]))
    )
    _, comparator, required_version = parse_requirement(REQUIRED_PYTHON_VERSION)

    if not comparator(current_python_version, required_version):
        print(
            f"Python version conflict: required {REQUIRED_PYTHON_VERSION}, found {'.'.join(map(str, current_python_version))}"
        )
        return False
    else:
        print(f"Python version found: {'.'.join(map(str, current_python_version))}")
        return True


def check_dependencies():
    python_version_ok = check_python_version()
    dependencies_missing = False

    for dependency in REQUIRED_DEPENDENCIES:
        package_name, comparator, required_version = parse_requirement(dependency)
        try:
            installed_version = parse_version_string(version(package_name))
            if comparator and not comparator(installed_version, required_version):
                print(
                    f"{package_name} version conflict: required {dependency}, found {'.'.join(map(str, installed_version))}"
                )
                dependencies_missing = True
            else:
                print(f"{package_name} found: {'.'.join(map(str, installed_version))}")
        except PackageNotFoundError:
            print(f"{package_name} not found.")
            dependencies_missing = True

    if not python_version_ok or dependencies_missing:
        print(
            "Some dependencies or the Python version are missing or have version conflicts. Please prepare the required dependencies with conda."
        )
        sys.exit(1)
    else:
        print("All dependencies and the Python version are correct.")


if __name__ == "__main__":
    check_dependencies()
