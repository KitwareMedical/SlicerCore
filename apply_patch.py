"""
This script generate a patched Slicer repository
The Slicer origin and ref are hardcoded as the patches are specific for a given Slicer version.

Usage:
    python generate_repo.py
    cd Slicer
    pip wheel .
"""

GIT_URL = "https://github.com/Slicer/Slicer.git"
GIT_REVISION = "8e556d8e1a20aa3d7af6a7f42d5ee669922c6d58"

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
import shutil


def execute_process(cmd: str, working_dir: str = ".") -> str:
    """Run a shell command and return the process standard output as a str"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            cwd=working_dir
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}", file=sys.stderr)
        print(f"Error message: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def is_patch(name: str) -> bool:
    return name.endswith((".patch"))


def mkpath(file: str) -> None:
    """Create the directories tree for given file path"""
    directory = os.path.dirname(file)
    if directory:
        os.makedirs(directory, exist_ok=True)


def apply_patch(file: str):
    """file is expected to be a relative path, it will be looked in both patch/ and Slicer/"""
    if is_patch(file):
        print(f"Applying patch {file}")
        execute_process(f"git apply ../patch/{file}", "Slicer")
    else:
        src = f"patch/{file}"
        dst = f"Slicer/{file}"
        print(f"Copying file from {src} to {dst}")
        mkpath(dst)
        shutil.copy2(src, dst)


def main() -> None:
    if not os.path.exists("patch"):
        print("No patch found. Patches must be stored in ./patch directory!")
        exit(1)

    if os.path.exists("Slicer"):
        print("Removing existing Slicer repository.")
        shutil.rmtree("Slicer")

    print(f"Cloning Slicer from {GIT_URL} at revision {GIT_REVISION} in the Slicer folder...")
    execute_process(f"git clone {GIT_URL} Slicer")
    execute_process(f"git checkout {GIT_REVISION}", "Slicer")

    for file in Path("patch").rglob("*"):
        if not os.path.isfile(file):
            continue

        apply_patch(str(Path(*file.parts[1:]))) # remove patch/


if __name__ == '__main__':
    main()
