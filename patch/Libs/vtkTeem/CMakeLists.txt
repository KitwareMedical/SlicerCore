# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

vtk_module_find_package(
  PACKAGE ITK
  COMPONENTS
    ITKCommon
    ITKVNL
)
include(${ITK_USE_FILE})

vtk_module_find_package(PACKAGE vtkAddon)

vtk_module_find_package(PACKAGE Teem PRIVATE_IF_SHARED)

# --------------------------------------------------------------------------
# Configure headers
# --------------------------------------------------------------------------
set(configure_header_file vtkTeemConfigure.h)
configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/${configure_header_file}.in
  ${CMAKE_CURRENT_BINARY_DIR}/${configure_header_file}
  )

slicercore_generate_module_wrapper(
  HEADER_NAME "vtkTeemModule.h"
  OUTPUT_VAR wrapper_header_file
)

# --------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------
set(classes
  vtkDiffusionTensorMathematics
  vtkDiffusionTensorGlyph
  vtkTeemNRRDReader
  vtkTeemNRRDWriter
  vtkImageLabelCombine
  )

set(headers
  ${CMAKE_CURRENT_BINARY_DIR}/${configure_header_file}
  ${wrapper_header_file}
)

vtk_module_add_module(Slicer::Teem
  EXPORT_MACRO_PREFIX VTK_Teem
  CLASSES ${classes}
  HEADERS ${headers}
)

vtk_module_link(Slicer::Teem
  PUBLIC
    ${ITK_LIBRARIES}
    vtkAddon
  PRIVATE
    Teem::teem
)
