
from __future__ import annotations

import os
from .venv import VEnv
from pathlib import Path
from typing import Optional
from shutil import copy2
from logging import warning

import pytest


def pytest_addoption(parser: pytest.Parser):
    # Register the custom argument
    parser.addoption(
        "--local-wheels", 
        action="store",
        type=Path,
        help="If set to existing directory, do not try to build slicer-core[-sdk] and use existing wheels only."
    )


@pytest.fixture(scope="session")
def curdir() -> Path:
    return Path(__file__).parent.resolve()


# Session-wide virtualenv with CMake, use this to build C++ projects independently
@pytest.fixture(scope="session")
def buildenv(tmp_path_factory: pytest.TempPathFactory) -> VEnv:
    path = tmp_path_factory.mktemp("cmake_env")
    venv = VEnv(path)
    venv.install("cmake")
    return venv


# Session-wide location to store built wheels
# Only build wheels once, then store them here (pip wheel ... --wheel-dir ${wheelhouse})
@pytest.fixture(scope="session")
def wheelhouse(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("wheelhouse")


# Slicer core is massive, we don't want to build the wheels if we already have them
def _copy_wheel(wheel_path: Path, glob_expr: str, dest: Path):
    if not wheel_path.exists():
        raise FileNotFoundError(wheel_path)
    
    candidates = [p for p in wheel_path.glob(glob_expr)]
    if len(candidates) > 1:
        candidate_list = [f"- {c}\n" for c in candidates]
        warning(f"Multiple candidates were found in path {wheel_path}.\n{candidate_list}\nSelected wheel \"{candidates[0]}\"\n")
    elif len(candidates) == 0:
        raise FileNotFoundError(f"Could not find {glob_expr} in folder \"{wheel_path}\".")

    copy2(candidates[0], dest)


# Build slicer_core wheel and store it in *wheelhouse*
@pytest.fixture(scope="session")
def slicer_core(buildenv: VEnv, curdir: Path, wheelhouse: Path, request: pytest.FixtureRequest) -> None:
    wheel_path : Optional[Path] = request.config.getoption("--local-wheels", default=None)
    if wheel_path is None:
        slicer_core_src = (curdir.parent.parent.resolve()).as_posix()
        buildenv.module(
            "pip", "wheel", slicer_core_src,
            "--wheel-dir", wheelhouse.as_posix(),
            "--extra-index-url", "https://vtk.org/files/wheel-sdks",
            "--extra-index-url", "https://wheels.vtk.org",
            "--verbose"
        )
    else:
        # use local wheelhouse, propagate to tmp wheelhouse so it looks like it was just built
        _copy_wheel(wheel_path, "slicer_core-*.whl", wheelhouse)


# Build slicer_core_sdk wheel and store it in *wheelhouse*
@pytest.fixture(scope="session")
def slicer_core_sdk(buildenv: VEnv, curdir: Path, wheelhouse: Path, request: pytest.FixtureRequest) -> None:
    wheel_path : Optional[Path] = request.config.getoption("--local-wheels", default=None)
    if wheel_path is None:
        slicer_core_sdk_src = (curdir.parent.resolve()).as_posix()
        buildenv.module(
            "pip", "wheel", slicer_core_sdk_src,
            "--wheel-dir", wheelhouse.as_posix(),
            "--extra-index-url", "https://vtk.org/files/wheel-sdks",
            "--extra-index-url", "https://wheels.vtk.org",
            "--verbose"
        )
    else:
        # use local wheelhouse, propagate to tmp wheelhouse so it looks like it was just built
        _copy_wheel(wheel_path, "slicer_core_sdk-*.whl", wheelhouse)


# Temporary virtualenv for the test projects
@pytest.fixture()
def virtualenv(tmp_path: Path) -> VEnv:
    path = tmp_path / "venv"
    return VEnv(path)
