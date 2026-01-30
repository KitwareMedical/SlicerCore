# How to wrap a loadable module:

### Wrappable

Logic, MRML, MRMLDM and VTKWidgets.

### Add vtk.module

```
NAME
  VTK::Slicer[name]Module[part]
LIBRARY_NAME
  vtkSlicer[name]Module[part]
DEPENDS
  ...
DESCRIPTION
  "vtkSlicer[name]Module[part]"
```

### Rework CMakeLists.txt

Look at old `find_package`, `target_link_libraries` and `target_include_directories` for dependencies.

```cmake
project(Slicer[name]Module[part])

find_package(dependencies... REQUIRED)

set(classes
    ... source files
  )

vtk_module_add_module(Slicer::[name]Module[part]
  EXPORT_MACRO_PREFIX VTK_SLICER_[NAME]_MODULE_[PART]
  CLASSES ${classes}
)

vtk_module_include(Slicer::[name]Module[part] ...)
vtk_module_link(Slicer::[name]Module[part] ...)
```

### Change export file include

Replace "vtkSlicer[name]Module[part]Export" with
