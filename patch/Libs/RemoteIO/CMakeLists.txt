# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------

vtk_module_find_package(
  PACKAGE CURL
  PRIVATE_IF_SHARED
)

if(Slicer_USE_PYTHONQT_WITH_OPENSSL)
  vtk_module_find_package(
    PACKAGE OpenSSL
    PRIVATE_IF_SHARED
  )
endif()

vtk_module_find_package(PACKAGE vtkAddon)

# --------------------------------------------------------------------------
# Configure headers
# --------------------------------------------------------------------------

set(configure_header_file vtkRemoteIOConfigure.h)
configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/${configure_header_file}.in
  ${CMAKE_CURRENT_BINARY_DIR}/${configure_header_file}
  )

slicercore_generate_module_wrapper(
  HEADER_NAME "vtkRemoteIOModule.h"
  OUTPUT_VAR wrapper_header_file
)

# --------------------------------------------------------------------------
# Build library
# --------------------------------------------------------------------------

set(classes vtkHTTPHandler)
set(headers
  ${CMAKE_CURRENT_BINARY_DIR}/${configure_header_file}
  ${wrapper_header_file}
)

vtk_module_add_module(Slicer::RemoteIO
  EXPORT_MACRO_PREFIX VTK_RemoteIO
  CLASSES ${classes}
  HEADERS ${headers}
)

vtk_module_link(Slicer::RemoteIO PUBLIC vtkAddon PRIVATE ${CURL_LIBRARIES})
vtk_module_include(Slicer::RemoteIO PRIVATE ${CURL_INCLUDE_DIRS})

if(WIN32)
  # Define CURL_STATICLIB when linking against static curl on Windows
  vtk_module_definitions(Slicer::RemoteIO PRIVATE CURL_STATICLIB)
  vtk_module_link(Slicer::RemoteIO PRIVATE iphlpapi ws2_32)
endif()
