"""
This creates a venv and does pip install slicer_core_sdk in it, then build another project that consummes the sdk
"""

from pathlib import Path
from .venv import VEnv

def test_find_package(virtualenv: VEnv, curdir: Path, wheelhouse: Path, slicer_core_sdk):
    test_src = (curdir / "packages" / "find_package").as_posix()
    virtualenv.module(
        "pip", "install", test_src,
        "--find-links", wheelhouse.as_posix(),
        "--extra-index-url", "https://vtk.org/files/wheel-sdks",
        "--extra-index-url", "https://wheels.vtk.org",
        "--verbose"
    )
