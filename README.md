# SlicerCore

SlicerCore (formally known as VTK MRML), is an alternative build-system for the 3DSlicer project
that is intended to build a Python Package (wheel) from the core libraries of 3DSlicer (a.k.a MRML).

## How it works

SlicerCore repository only contains patches against a known version of Slicer.

SlicerCore patches replaces 3DSlicer build system (`CMakeLists.txt`), introduces `vtk.module` files.
There are a small amount of modification done on the C++ code too, but the goal is to do the minimum amount of changes in it.

Patches are generated from [my (Alexy Pellegrini) fork](https://github.com/AlexyPellegrini/Slicer/tree/slicer-core-5-12)
using the `SlicerCore/generate_patch.py` script on said fork.
Patches are then applied on the same revision using the `apply_patch.py` (on this repo).

This creates a source tree: `./Slicer` that contains the patched Slicer ready to be built.

## Building

To build slicer-core wheel:
```sh
python -m pip wheel Slicer --extra-index-url https://vtk.org/files/wheel-sdks
```

To build slicer-core-sdk wheel:
```sh
python -m pip wheel Slicer/SlicerCoreSDK --extra-index-url https://vtk.org/files/wheel-sdks
```

To run SlicerCoreSDK tests:
```sh
python -m pip install virtualenv pytest
python -m pytest Slicer/SlicerCoreSDK
```

Note that SlicerCoreSDK tests will by default build SlicerCore and SlicerCoreSDK from scratch, and that takes about an hour even on a decent hardware.
An optional option is supported by the tests: --local-wheels, so you can built the wheels then test them without any additional build.

Typical workflow would be:
```sh
# Install build deps
python -m pip install virtualenv pytest
# Build the twos wheels
python -m pip wheel Slicer --wheel-dir wheelhouse --extra-index-url https://vtk.org/files/wheel-sdks
python -m pip wheel Slicer/SlicerCoreSDK --wheel-dir wheelhouse --extra-index-url https://vtk.org/files/wheel-sdks
# Test them
python -m pytest Slicer/SlicerCoreSDK --local-wheels wheelhouse
```

### Patching the wheels

SlicerCore and its SDK can not be patched using the classic auditwheel, delvewheel or relocate.</br>
Everything is already patched and installed as needed by the CMake code.

To have a wheel that is properly tagged, force the tag of the building OS:
```sh
python -m pip install wheel
python -m wheel tags --platform-tag <your-platform> --remove wheelhouse/slicer_core-*.whl
python -m wheel tags --platform-tag <your-platform> --remove wheelhouse/slicer_core_sdk-*.whl
```

This step is only needed on Linux and Mac.

## How to use

While you may use SlicerCore as-is, it is indended to be the base of [trame-slicer](https://github.com/KitwareMedical/trame-slicer).

## License

Apache License, Version 2.0.
See LICENSE file for details.
