set(classes vtkSlicerColorLogic)

slicercore_generate_module_wrapper(
  HEADER_NAME "vtkSlicerColorsModuleLogicExport.h"
  OUTPUT_VAR wrapper_header_file
)

vtk_module_add_module(Slicer::ColorsModuleLogic
  EXPORT_MACRO_PREFIX VTK_SLICER_COLORS_MODULE_LOGIC
  CLASSES ${classes}
  HEADERS ${wrapper_header_file}
)
