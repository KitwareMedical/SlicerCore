"""
Script to generate a patch composed of multiple files based on git diff.

Usage:
    python generate_patch.py
"""

import os
from pathlib import Path
from typing import List, Tuple
import shutil
from enum import Enum

from common import execute_process, mkpath

class DiffCategory(Enum):
    ADDED = "A"
    MODIFIED = "M"


DIFF_CATEGORY_VALUES = set(item.value for item in DiffCategory)


def is_cmake_file(name: str) -> bool:
    return name.endswith((".cmake", ".cmake.in", "CMakeLists.txt", "vtk.module"))


def is_cpp_file(name: str) -> bool:
    return name.endswith((".h", ".h.in", ".cxx", ".cxx.in", ".hxx", ".hxx.in"))


def analyze_line(line: str) -> Tuple[DiffCategory, str]:
    status, file_path = line.split('\t')
    if status not in DIFF_CATEGORY_VALUES:
        raise Exception(f"Status of \"{file_path}\" is not a valid, must be one of {DIFF_CATEGORY_VALUES}")
    # Assume path exists, git won't lie to us...
    return (DiffCategory(status), file_path)


def get_changed_files(git_ref: str, cwd: str) -> List[Tuple[DiffCategory, str]]:
    """Get the list of changed files using git diff --name-status."""
    diff = execute_process(f"git diff --name-status {git_ref}", cwd)
    return [analyze_line(line) for line in diff.strip().split('\n')]


def copy_file(source: Path, destination: Path) -> None:
    """Copy a file from source to destination."""
    try:
        mkpath(destination)
        shutil.copy2(source, destination)
    except Exception as e:
        raise Exception(f"Error copying {source}: {e}")


def generate_patch(git_ref: str, input_folder: str, file_path: str, output_path: str) -> None:
    """Generate a patch file for the given file."""
    try:
        patch_content = execute_process(f"git diff {git_ref} -- {file_path}", input_folder)
        mkpath(output_path)
        with open(output_path, 'w') as f:
            f.write(patch_content)
    except Exception as e:
        raise Exception(f"Error writing patch for {file_path}: {e}")


def process_files(git_ref: str, input_folder: str, output_folder: str, changed_files: List[Tuple[DiffCategory, str]]) -> None:
    """ Process all changed files
    CMake file: Always copy it, it will replace the original file
    C++ file: Make a patch if it modified, copy it if it was added
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    for status, file_path in changed_files:
        input_file = input_path / file_path
        output_file = output_path / file_path
        
        match status:
            case DiffCategory.MODIFIED:
                if is_cmake_file(file_path):
                    # Copy CMakeLists.txt or *.cmake files
                    copy_file(input_file, output_file)
                elif is_cpp_file(file_path):
                    # Generate patch for other modified files
                    patch_file = str(output_file) + '.patch'
                    generate_patch(git_ref, input_folder, file_path, patch_file)
                else:
                    print(f"Warning: Ignoring unknown file {file_path}")
            case DiffCategory.ADDED:
                copy_file(input_file, output_file)


def main() -> None:
    from common import GIT_REVISION, SLICER_DIR, PATCH_DIR

    if not Path(SLICER_DIR).exists():
        print(f"{SLICER_DIR} folder does not exist. Please run apply_patch.py first.")
        exit(1)

    # Prevent generation if there are uncommited changes, this prevent mistakes as it forces user to commit first.
    if len(execute_process("git diff", SLICER_DIR)) != 0:
        print("Error: You have unstagged changes. Please stash or commit them.")
        exit(1)

    # Verify git reference exists (git returns non-zero if that the case)
    execute_process(f"git rev-parse {GIT_REVISION}", SLICER_DIR)

    # Notice about that, this is a correct behavior but 
    if os.path.exists(PATCH_DIR):
        print("Patch folder exists, it won't be cleared!"
            "If you removed files you must clear it before generating patches."
            "Alternatively, you can manually remove such files in patch folder.")
    
    changed_files = get_changed_files(GIT_REVISION, SLICER_DIR)
    if not changed_files:
        print("Nothing to do.")
        exit(0)
    
    # Process all files
    process_files(GIT_REVISION, SLICER_DIR, PATCH_DIR, changed_files)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error occured while generating patch:\n{e}")
        exit(1)