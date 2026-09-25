from common import SLICER_DIR
from pathlib import Path
import re
import sys


# This is a simple regex that matches most valid python package version
VERSION_PATTERN = r'([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?'
# List of (package name, file) pairs to replace version in
FILES = [
    ("vtk", Path(SLICER_DIR) / "SlicerCore" / "pyproject.toml"),
    ("vtk-sdk", Path(SLICER_DIR) / "SlicerCore" / "pyproject.toml"),
    ("vtk-sdk", Path(SLICER_DIR) / "SlicerCore" / "tests" / "packages" / "build_module" / "pyproject.toml"),
    ("vtk-sdk", Path(SLICER_DIR) / "SlicerCore" / "tests" / "packages" / "find_package" / "pyproject.toml"),
    ("vtk", Path(SLICER_DIR) / "SlicerCoreSDK" / "pyproject.toml"),
    ("vtk-sdk", Path(SLICER_DIR) / "SlicerCoreSDK" / "pyproject.toml"),
    ("vtk", Path(__file__).parent / "build_requirements.txt"),
    ("vtk-sdk", Path(__file__).parent / "build_requirements.txt"),
]


def patch_version(pyproject: Path, name: str, version: str):
    """Replace occurence of {name}==X.Y.Z with {name}=={version} in file {pyproject}"""
    print(f"Replacing occurence of {name}==X.Y.Z with {name}=={version} in file {pyproject}")
    new_content = ""
    with open(pyproject, "r") as file:
        new_content = re.sub(f"{name}=={VERSION_PATTERN}", f"{name}=={version}", file.read())
    with open(pyproject, "w") as file:
        file.write(new_content)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python set_vtk_version.py <vtk-version>")
        exit(1)

    version = sys.argv[1]
    if not re.match(VERSION_PATTERN, version):
        print(f"Given version, {version}, is not a valid version identifier")
        exit(1)

    for package, file in FILES:
        patch_version(file, package, version)


if __name__ == '__main__':
    main()
