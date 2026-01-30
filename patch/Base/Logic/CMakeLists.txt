# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

vtk_module_find_package(
  PACKAGE SlicerExecutionModel
  COMPONENTS ModuleDescriptionParser
  PRIVATE_IF_SHARED
)
vtk_module_find_package(
  PACKAGE LibArchive
  PRIVATE_IF_SHARED
)

vtk_module_find_package(
  PACKAGE ITK
  COMPONENTS
    ITKCommon
    ITKIOTransformBase
    ITKTransform
    ${ModuleDescriptionParser_ITK_COMPONENTS}
)
include(${ITK_USE_FILE})

vtk_module_find_package(PACKAGE vtkAddon)

# --------------------------------------------------------------------------
# Subdirectories
# --------------------------------------------------------------------------
add_subdirectory(Resources)

#--------------------------------------------------------------------
# Configure headers
# --------------------------------------------------------------------------
set(configure_header_file vtkSlicerBaseLogicConfigure.h)
configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/${configure_header_file}.in
  ${CMAKE_CURRENT_BINARY_DIR}/${configure_header_file}
)

# --------------------------------------------------------------------------
# Build library
# --------------------------------------------------------------------------
set(classes
  # Logic classes (data management and calculation)
  vtkSlicerApplicationLogic
  vtkSlicerModuleLogic
  vtkSlicerTask
  vtkDataIOManagerLogic
  # Slicer's VTK extensions (filters)
  vtkTransformVisualizerGlyph3D
  vtkImageRectangularSource
  vtkSystemInformation
  vtkImageFillROI
  vtkSlicerCLIModuleLogic
  vtkSlicerScriptedLoadableModuleLogic
)

set(headers
  vtkSlicerBaseLogic.h
  vtkSlicerBaseLogicExport.h
  ${CMAKE_CURRENT_BINARY_DIR}/${configure_header_file}
)

vtk_module_add_module(Slicer::BaseLogic
  EXPORT_MACRO_PREFIX VTK_SLICER_BASE_LOGIC
  CLASSES ${classes}
  HEADERS ${headers}
)

vtk_module_link(Slicer::BaseLogic
  PUBLIC
    ${ITK_LIBRARIES} vtkAddon
  PRIVATE
    ModuleDescriptionParser
    ${LibArchive_LIBRARY}
)

vtk_module_include(Slicer::BaseLogic
  PRIVATE
    ${ModuleDescriptionParser_INCLUDE_DIRS}
    ${LibArchive_INCLUDE_DIRS}
)
