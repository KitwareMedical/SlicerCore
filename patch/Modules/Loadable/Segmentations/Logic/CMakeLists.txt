project(vtkSlicerSegmentationsModuleLogic)

set(classes
  vtkSlicerSegmentationsModuleLogic
  vtkSlicerSegmentationGeometryLogic
  vtkImageGrowCutSegment
  FibHeap
  vtkSlicerSegmentEditorLogic
)

slicercore_generate_module_wrapper(
  HEADER_NAME "vtkSlicerSegmentationsModuleLogicExport.h"
  OUTPUT_VAR wrapper_header_file
)

vtk_module_add_module(Slicer::SegmentationsModuleLogic
  EXPORT_MACRO_PREFIX VTK_SLICER_SEGMENTATIONS_LOGIC
  CLASSES ${classes}
  HEADERS ${wrapper_header_file}
)
