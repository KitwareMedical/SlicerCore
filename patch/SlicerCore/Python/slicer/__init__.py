"""
Meta-package for 3DSlicer related package

## Brief

    This package is an entry-point that enable users to import slicer-based modules
    into a unique namespace "slicer":
    For example: `from slicer import ...` -> can access all registered modules

## Registering a package in the "slicer" meta-package

    To register a module as a slicer module, one needs to add a slicer_*.py module in this folder
    at wheel install time: 
    ```py
    # slicer/slicer_core.py
    from slicer_core import *
    --------------------------------
    # slicer_core/__init__.py
    from .MRMLCore import *
    ```

    This meta-package also supports runtime injection using PYTHONPATH.
    By adding a path ending with "slicer" in `PYTHONPATH`, this package will find all modules
    in this said folder, so previous approach can be used the same way:
    ```
    # some-path-specified-in-PYTHONPATH/slicer/slicer_mymodule.py
    from slicer_mymodule import *
    --------------------------------
    # some-path-specified-in-PYTHONPATH/slicer_mymodule/__init__.py
    from .MyModule import *
    ```
    Note that this slicer folder MUST NOT contain a `__init__.py` file!

## Notes

    - "slicer" meta-package is part of `slicer-core` package, and will be removed if uninstalled!
"""

import sys
from importlib import import_module
from pkgutil import iter_modules, extend_path

# This enables other "slicer" packages to be found,
# allowing users to inject slicer modules from outside site-packages
# using PYTHONPATH or similar.
__path__ = extend_path(__path__, __name__)

# Loop over all module in "slicer" packages, these modules are expected to be jump pads to other packages
me = sys.modules[__name__]
for info in iter_modules(__path__):
    module = import_module(f"{__name__}.{info.name}")
    for item_name in dir(module):
        # Exclude any private (_x) and builtin (__x) symbols
        if item_name.startswith("_"):
            continue
        # propagate attributes to the "slicer" module
        setattr(me, item_name,  getattr(module, item_name))
