list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR})
find_package(JsonCpp REQUIRED)

set(classes
  vtkMRMLCPURayCastVolumeRenderingDisplayNode
  vtkMRMLGPURayCastVolumeRenderingDisplayNode
  vtkMRMLMultiVolumeRenderingDisplayNode
  vtkMRMLShaderPropertyNode
  vtkMRMLShaderPropertyStorageNode
  vtkMRMLVolumePropertyJsonStorageNode
  vtkMRMLVolumePropertyNode
  vtkMRMLVolumePropertyStorageNode
  vtkMRMLVolumeRenderingDisplayNode
)

slicercore_generate_module_wrapper(
  HEADER_NAME "vtkSlicerVolumeRenderingModuleMRMLExport.h"
  OUTPUT_VAR wrapper_header_file
)

vtk_module_add_module(Slicer::VolumeRenderingModuleMRML
  EXPORT_MACRO_PREFIX VTK_SLICER_VOLUMERENDERING_MODULE_MRML
  CLASSES ${classes}
  HEADERS ${wrapper_header_file}
)

vtk_module_include(Slicer::VolumeRenderingModuleMRML PUBLIC ${JsonCpp_INCLUDE_DIRS})
vtk_module_link(Slicer::VolumeRenderingModuleMRML PUBLIC ${JsonCpp_LIBRARY})
