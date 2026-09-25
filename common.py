# Baseline Slicer repository, change this when rebasing
GIT_URL = "https://github.com/Slicer/Slicer.git"
GIT_REVISION = "9a54dda46fdd0db1438711adb7add9ba85bce331" # 2026/09/25

# Directories used by the scripts
SLICER_DIR = "Slicer"
PATCH_DIR = "patch"

import subprocess
import os

def execute_process(cmd: str, cwd: str = ".") -> str:
    """Run a shell command and return the process standard output as a str.
    Throws an exception with subprocess stderr if return code is not zero.
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running command: {cmd}\nError message:\n{e.stderr}\n")


def mkpath(file_path: str) -> None:
    """Create the directories tree for given file path"""
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

