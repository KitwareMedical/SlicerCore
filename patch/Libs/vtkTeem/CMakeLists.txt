# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

#
# ITK
#
set(${PROJECT_NAME}_ITK_COMPONENTS
  ITKCommon
  ITKVNL
  )
find_package(ITK 5.0 COMPONENTS ${${PROJECT_NAME}_ITK_COMPONENTS} REQUIRED)
include(${ITK_USE_FILE})

#
# Teem
#
find_package(Teem REQUIRED NO_MODULE)
# XXX Since no TeemConfigVersion.cmake is configured, let's check the version explicitly
if(${Teem_VERSION_MAJOR}.${Teem_VERSION_MINOR}.${Teem_VERSION_PATCH} VERSION_LESS 1.10)
  message(FATAL_ERROR
    "Could not find a configuration file for package \"Teem\" that is compatible with requested version \"1.10\".")
endif()
include(${Teem_USE_FILE})

# XXX Teem 1.11.0 or Teem >= 4168 - This variable won't be needed anymore.
#     See https://sourceforge.net/p/teem/code/4168/
set(Teem_LIBRARIES teem)

#
# vtkAddon
#
find_package(vtkAddon REQUIRED)

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

vtk_module_link(Slicer::Teem PUBLIC ${ITK_LIBRARIES} ${Teem_LIBRARIES} vtkAddon)
vtk_module_include(Slicer::Teem PUBLIC ${Teem_INCLUDE_DIRS} ${vtkAddon_INCLUDE_DIRS})
