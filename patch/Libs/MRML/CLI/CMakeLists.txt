# ModuleDescriptionParser
find_package(SlicerExecutionModel REQUIRED ModuleDescriptionParser)

# ITK - Import ITK targets required by ModuleDescriptionParser
find_package(ITK 5.3 COMPONENTS ${ModuleDescriptionParser_ITK_COMPONENTS} REQUIRED)

slicercore_generate_module_wrapper(
  HEADER_NAME "vtkMRMLCLIModule.h"
  OUTPUT_VAR wrapper_header_file
)

set(classes vtkMRMLCommandLineModuleNode)

vtk_module_add_module(Slicer::MRMLCLI
  EXPORT_MACRO_PREFIX VTK_MRML_CLI
  CLASSES ${classes}
  HEADERS ${wrapper_header_file}
)

vtk_module_link(Slicer::MRMLCLI PUBLIC ${ITK_LIBRARIES} ModuleDescriptionParser)
vtk_module_include(Slicer::MRMLCLI PUBLIC ${ITK_INCLUDE_DIRS} ${ModuleDescriptionParser_INCLUDE_DIRS})
