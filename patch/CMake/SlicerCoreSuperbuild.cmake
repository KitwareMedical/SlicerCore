find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
# We need to normalize paths because CMake on Windows gives us paths with backslashes
# ExternalProject cache files contain `set("some\path")` which is badly interpreted...
cmake_path(CONVERT ${Python3_EXECUTABLE} TO_CMAKE_PATH_LIST Python3_EXECUTABLE NORMALIZE)
cmake_path(CONVERT ${Python3_LIBRARIES} TO_CMAKE_PATH_LIST Python3_LIBRARIES NORMALIZE)
cmake_path(CONVERT ${Python3_INCLUDE_DIR} TO_CMAKE_PATH_LIST Python3_INCLUDE_DIR NORMALIZE)

if(UNIX AND NOT APPLE AND CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64")
  # use the right as VTK enforces it
  # This is automatically handled for the package itself, but not for superbuild dependencies
  set(ep_common_cxx_flags "-D_GLIBCXX_USE_CXX11_ABI=0")
endif()

include(ExternalProject)
include(ExternalProjectDependency)
include(ExternalProjectGenerateProjectDescription)

# These are magic variables required for Superbuild scripts
set(EP_GIT_PROTOCOL "https") # some clones fail with git:
set(Slicer_BUILD_DICOM_SUPPORT "ON") # always build DICOM support
set(Slicer_USE_TBB "ON") # always use tbb
set(SLICERLIB_PYTHON_BUILD "TRUE") # used at some places to make changes in cmake logic
set(Slicer_USE_SYSTEM_VTK ON) # vtk comes from vtk-sdk

# Global build options
set(CMAKE_CXX_STANDARD "17")
set(CMAKE_CXX_STANDARD_REQUIRED "ON")
set(CMAKE_CXX_EXTENSIONS "OFF")
set(CMAKE_POSITION_INDEPENDENT_CODE "TRUE")

mark_as_superbuild(
  VARS
    # Global build options
    BUILD_SHARED_LIBS
    CMAKE_BUILD_TYPE
    CMAKE_CXX_STANDARD
    CMAKE_CXX_STANDARD_REQUIRED
    CMAKE_CXX_EXTENSIONS
    CMAKE_CXX_FLAGS_DEBUG
    CMAKE_CXX_FLAGS_RELEASE
    CMAKE_CXX_FLAGS_RELWITHDEBINFO
    CMAKE_CXX_FLAGS_MINSIZEREL
    CMAKE_POSITION_INDEPENDENT_CODE
    # forward VTK and other prefixes
    CMAKE_PREFIX_PATH
    # Forward main scikit-build core properties
    SKBUILD_STATE
    SKBUILD_PROJECT_NAME
    SKBUILD_PROJECT_VERSION
    SKBUILD_PROJECT_VERSION_FULL
  ALL_PROJECTS
  )

# Forward used linker if any
if(DEFINED CMAKE_LINKER_TYPE)
  mark_as_superbuild(VARS CMAKE_LINKER_TYPE ALL_PROJECTS)
endif()

if(CMAKE_VERSION VERSION_GREATER_EQUAL 4.0)
  set(CMAKE_POLICY_VERSION_MINIMUM 3.5)
  mark_as_superbuild(VARS CMAKE_POLICY_VERSION_MINIMUM ALL_PROJECTS)
endif()

if(APPLE)
  mark_as_superbuild(VARS
    CMAKE_OSX_ARCHITECTURES:STRING
    CMAKE_OSX_SYSROOT:PATH
    CMAKE_OSX_DEPLOYMENT_TARGET:STRING
    ALL_PROJECTS
    )
endif()

# TODO: doc
if(DEFINED EXTERNAL_PROJECT_CMAKE_CACHE_ARGS)
  foreach(varname IN LISTS EXTERNAL_PROJECT_CMAKE_CACHE_ARGS)
    if(DEFINED ${varname})
      mark_as_superbuild(${varname})
    endif()
  endforeach()
endif()

# This is all the dependencies required for the slicer-core wheel
set(dependencies
  curl
  DCMTK
  ITK
  JsonCpp
  LibArchive
  ParameterSerializer
  RapidJSON
  SlicerExecutionModel
  tbb
  teem
  vtkAddon
)

message(STATUS "Looking for dependencies in folder ${EXTERNAL_PROJECT_DIR}")
set(proj ${SKBUILD_PROJECT_NAME})
set(SUPERBUILD_TOPLEVEL_PROJECT ${proj})
mark_as_superbuild(dependencies:STRING)

ExternalProject_Include_Dependencies(${proj} PROJECT_VAR proj DEPENDS_VAR dependencies SUPERBUILD_VAR USE_SUPERBUILD)

ExternalProject_Add(${proj}
  ${${proj}_EP_ARGS}
  DEPENDS ${dependencies}
  SOURCE_DIR ${CMAKE_SOURCE_DIR}
  BINARY_DIR ${CMAKE_BINARY_DIR}/inner-build
  CMAKE_CACHE_ARGS
    -DCMAKE_CXX_COMPILER:FILEPATH=${CMAKE_CXX_COMPILER}
    -DCMAKE_CXX_FLAGS:STRING=${CMAKE_CXX_FLAGS}
    -DCMAKE_C_COMPILER:FILEPATH=${CMAKE_C_COMPILER}
    -DCMAKE_C_FLAGS:STRING=${CMAKE_C_FLAGS}
    -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}
    -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
    -DUSE_SUPERBUILD:BOOL=OFF
    ${EXTERNAL_PROJECT_OPTIONAL_CMAKE_CACHE_ARGS}
  INSTALL_COMMAND ""
  )
ExternalProject_AlwaysConfigure(${proj})

# Forward install code from inner build to this project
install(CODE "include(\"${CMAKE_BINARY_DIR}/inner-build/cmake_install.cmake\")")
