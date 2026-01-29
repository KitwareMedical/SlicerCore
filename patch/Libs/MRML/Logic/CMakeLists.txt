# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

#
# ITK
#
set(${PROJECT_NAME}_ITK_COMPONENTS
  ITKCommon
)
find_package(ITK 4.6 COMPONENTS ${${PROJECT_NAME}_ITK_COMPONENTS} REQUIRED)
include(${ITK_USE_FILE})

# --------------------------------------------------------------------------
# Configure headers
# --------------------------------------------------------------------------
set(configure_header_file vtkMRMLLogicConfigure.h)
configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/${configure_header_file}.in
  ${CMAKE_CURRENT_BINARY_DIR}/${configure_header_file}
)

slicercore_generate_module_wrapper(
  HEADER_NAME "vtkMRMLLogicModule.h"
  OUTPUT_VAR wrapper_header_file
)

set(classes
  vtkMRMLAbstractLogic
  vtkMRMLApplicationLogic
  vtkMRMLColorLogic
  vtkMRMLDisplayableHierarchyLogic
  vtkMRMLRemoteIOLogic
  vtkMRMLLayoutLogic
  vtkMRMLSliceLayerLogic
  vtkMRMLSliceLogic
  vtkMRMLSliceLinkLogic
  vtkMRMLViewLogic
  vtkMRMLViewLinkLogic
  # slicer's vtk extensions (filters)
  vtkImageLabelOutline
  vtkImageNeighborhoodFilter
)

set(headers
  ${CMAKE_CURRENT_BINARY_DIR}/${configure_header_file}
  ${wrapper_header_file}
)

vtk_module_add_module(Slicer::MRMLLogic
  EXPORT_MACRO_PREFIX VTK_MRML_LOGIC
  CLASSES ${classes}
  HEADERS ${headers}
)

vtk_module_link(Slicer::MRMLLogic PUBLIC ${ITK_LIBRARIES})
vtk_module_include(Slicer::MRMLLogic PUBLIC ${ITK_INCLUDE_DIRS})
