"""
This creates a venv and does pip install BasicProject in it, then call a few python scripts
"""

from pathlib import Path
from .venv import VEnv

def test_import(virtualenv: VEnv, wheelhouse: Path, slicer_core):
    virtualenv.module("pip", "install", "slicer-core",
        "--find-links", wheelhouse.as_posix(), 
        "--extra-index-url", "https://vtk.org/files/wheel-sdks",
        "--extra-index-url", "https://wheels.vtk.org"
    )

    virtualenv.execute("from slicer_core import vtkMRMLNode; exit(0)")
    virtualenv.execute("import slicer_core; exit(int(hasattr(slicer_core, 'vtkmodules')))")
    virtualenv.execute("import slicer_core; from pathlib import Path; exit(0 if Path(slicer_core.__path__[0] + '/third_party.libs').is_dir() else 1)")
