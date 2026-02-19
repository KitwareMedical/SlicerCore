"""
This creates a venv and does pip install slicer_core_sdk in it, then build another project that consummes the sdk
"""

from pathlib import Path
from .venv import VEnv

def test_build_module(virtualenv: VEnv, curdir: Path, wheelhouse: Path, slicer_core, slicer_core_sdk):
    test_dir = curdir / "packages" / "build_module"
    virtualenv.module(
        "pip", "install", test_dir.as_posix(),
        "--find-links", wheelhouse.as_posix(),
        "--extra-index-url", "https://vtk.org/files/wheel-sdks",
        "--extra-index-url", "https://wheels.vtk.org",
        "--verbose"
    )

    virtualenv.run("python", (test_dir / "main.py").as_posix())
