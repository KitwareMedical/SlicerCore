"""
Script to generate a patch composed of multiple files based on git diff.

Usage:
    python generate_patch.py <git-ref> <prefix>

Example:
    python generate_patch.py origin/main patch_output
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
import shutil
from enum import Enum


class DiffCategory(Enum):
    ADDED = "A"
    MODIFIED = "M"


DIFF_CATEGORY_VALUES = set(item.value for item in DiffCategory)


def execute_process(cmd: str) -> str:
    """Run a shell command and return the process standard output as a str"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}", file=sys.stderr)
        print(f"Error message: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def is_cmake_file(name: str) -> bool:
    return name.endswith((".cmake", "CMakeLists.txt", "vtk.module"))


def is_cpp_file(name: str) -> bool:
    return name.endswith((".h", ".cxx", ".h.in", ".cxx.in"))


def analyze_line(line: str) -> Tuple[DiffCategory, str]:
    status, file_path = line.split('\t')
    if status not in DIFF_CATEGORY_VALUES:
        print(f"Status of \"{file_path}\" is not a valid, must be one of {DIFF_CATEGORY_VALUES}")
        exit(1)
    # Assume path exists, git won't lie to us...
    return (DiffCategory(status), file_path)


def get_changed_files(git_ref: str) -> List[Tuple[DiffCategory, str]]:
    """Get the list of changed files using git diff --name-status."""
    diff = execute_process(f"git diff --name-status {git_ref}")
    return [analyze_line(line) for line in diff.strip().split('\n')]


def mkpath(file_path: str) -> None:
    """Create the directories tree for given file path"""
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def copy_file(source: str, destination: str) -> None:
    """Copy a file from source to destination."""
    try:
        mkpath(destination)
        shutil.copy2(source, destination)
        print(f"Copied: {source} -> {destination}")
    except Exception as e:
        print(f"Error copying {source}: {e}", file=sys.stderr)


def generate_patch(git_ref: str, file_path: str, output_path: str) -> None:
    """Generate a patch file for the given file."""
    patch_content = execute_process(f"git diff {git_ref} -- {file_path}")
    
    try:
        mkpath(output_path)
        with open(output_path, 'w') as f:
            f.write(patch_content)
        print(f"Generated patch: {output_path}")
    except Exception as e:
        print(f"Error writing patch for {file_path}: {e}", file=sys.stderr)


def process_files(git_ref: str, output_folder: str, changed_files: List[Tuple[DiffCategory, str]]) -> None:
    """ Process all changed files
    
    If the file is a CMake file (vtk.module, CMakeLists.txt or *.cmake):
        Always copy it, it will replace the original file
    If the file is a C++ file (*.h, *.cxx, *.h.in, *.cxx.in):
        Make a patch if it modified, copy it if it was added
    """
    output_path = Path(output_folder)
    
    for status, file_path in changed_files:
        output_file = output_path / file_path
        
        match status:
            case DiffCategory.MODIFIED:
                if is_cmake_file(file_path):
                    # Copy CMakeLists.txt or *.cmake files
                    copy_file(file_path, str(output_file))
                elif is_cpp_file(file_path):
                    # Generate patch for other modified files
                    patch_file = str(output_file) + '.patch'
                    generate_patch(git_ref, file_path, patch_file)
                else:
                    print(f"Ignoring unknown file {file_path}")
            case DiffCategory.ADDED:
                copy_file(file_path, str(output_file))


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate a patch composed of multiple files based on git diff.'
    )
    parser.add_argument(
        "git_ref",
        help='Git reference to compare against (e.g., origin/main, HEAD~1, commit-sha)'
    )
    parser.add_argument(
        "prefix",
        help='Output folder where patch files will be generated'
    )
    
    args = parser.parse_args()
    
    # Prevent generation if there are uncommited changes
    if len(execute_process("git diff")) != 0:
        print("You have unstagged changes. Please stash or commit them.")
        exit(1)

    # Verify we're in a git repository and given git reference exists (git returns non-zero if that the case)
    execute_process(f"git rev-parse {args.git_ref}")

    changed_files = get_changed_files(args.git_ref)
    if not changed_files:
        print("Nothing to do. Please check git ref.")
        return
    
    if os.path.exists(args.prefix):
        print("Prefix already exists, it won't be cleared.")
    
    # Process all files
    process_files(args.git_ref, args.prefix, changed_files)
    

if __name__ == '__main__':
    main()