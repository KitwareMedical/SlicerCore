
set(proj vtkAddon)

# Set dependency list
set(${proj}_DEPENDENCIES VTK)

# Include dependent projects if any
ExternalProject_Include_Dependencies(${proj} PROJECT_VAR proj DEPENDS_VAR ${proj}_DEPENDENCIES)

if(NOT DEFINED vtkAddon_DIR AND NOT Slicer_USE_SYSTEM_${proj})

  ExternalProject_SetIfNotDefined(
    Slicer_${proj}_GIT_REPOSITORY
    "${EP_GIT_PROTOCOL}://github.com/AlexyPellegrini/vtkAddon.git"
    QUIET
  )

  ExternalProject_SetIfNotDefined(
    Slicer_${proj}_GIT_TAG
    "python-dev-cmake"
    QUIET
  )

  cmake_path(CONVERT Python_EXECUTABLE TO_CMAKE_PATH_LIST Python_EXECUTABLE NORMALIZE)
  set(EXTERNAL_PROJECT_OPTIONAL_CMAKE_CACHE_ARGS)

  if(SLICERLIB_PYTHON_BUILD)
    list(APPEND EXTERNAL_PROJECT_OPTIONAL_CMAKE_CACHE_ARGS
      "-DCMAKE_PREFIX_PATH:PATH=${CMAKE_PREFIX_PATH}"
      "-DvtkAddon_WRAP_PYTHON:BOOL=ON"
      "-DPYTHON_EXECUTABLE:FILEPATH=${Python3_EXECUTABLE}"
      "-DPYTHON_LIBRARY:FILEPATH=${Python3_LIBRARIES}"
      "-DPYTHON_INCLUDE_DIRS:PATH=${Python3_INCLUDE_DIR}"
    )
  else()
    # when building slicer we need to specify the Python instance
    list(APPEND EXTERNAL_PROJECT_OPTIONAL_CMAKE_CACHE_ARGS
      "-DvtkAddon_WRAP_PYTHON:BOOL=${Slicer_USE_PYTHONQT}"
      "-DPYTHON_EXECUTABLE:FILEPATH=${PYTHON_EXECUTABLE}"
      "-DPYTHON_LIBRARY:FILEPATH=${PYTHON_LIBRARY}"
      "-DPYTHON_INCLUDE_DIR:PATH=${PYTHON_INCLUDE_DIR}"
    )
  endif()

  list(APPEND vtkAddon_CMAKE_CACHE_ARGS)

  set(EP_SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj})
  set(EP_BINARY_DIR ${CMAKE_BINARY_DIR}/${proj}-build)
  set(EP_INSTALL_DIR ${EP_DEPENDENCIES_INSTALL_DIR})

  ExternalProject_Add(${proj}
    ${${proj}_EP_ARGS}
    GIT_REPOSITORY "${Slicer_${proj}_GIT_REPOSITORY}"
    GIT_TAG "${Slicer_${proj}_GIT_TAG}"
    SOURCE_DIR ${EP_SOURCE_DIR}
    BINARY_DIR ${EP_BINARY_DIR}
    CMAKE_CACHE_ARGS
      -DCMAKE_CXX_COMPILER:FILEPATH=${CMAKE_CXX_COMPILER}
      -DCMAKE_CXX_FLAGS:STRING=${ep_common_cxx_flags}
      -DCMAKE_C_COMPILER:FILEPATH=${CMAKE_C_COMPILER}
      -DCMAKE_C_FLAGS:STRING=${ep_common_c_flags}
      -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
      -DCMAKE_INSTALL_PREFIX:PATH=${EP_INSTALL_DIR}
      -DBUILD_SHARED_LIBS:BOOL=ON
      -DBUILD_TESTING:BOOL=OFF
      -DvtkAddon_USE_UTF8:BOOL=ON
      -DvtkAddon_CMAKE_DIR:PATH=${EP_SOURCE_DIR}/CMake
      -DvtkAddon_LAUNCH_COMMAND:STRING=${Slicer_LAUNCH_COMMAND}
      -DVTK_WRAP_PYTHON_FIND_LIBS:BOOL=OFF
      -DVTK_DIR:PATH=${VTK_DIR}
      ${vtkAddon_CMAKE_CACHE_ARGS}
      ${EXTERNAL_PROJECT_OPTIONAL_CMAKE_CACHE_ARGS}
    DEPENDS
      ${${proj}_DEPENDENCIES}
  )

  ExternalProject_GenerateProjectDescription_Step(${proj})

  set(vtkAddon_DIR ${EP_INSTALL_DIR}/lib/CMake/vtkAddon)

  # Add path to SlicerLauncherSettings.ini
  set(${proj}_LIBRARY_PATHS_LAUNCHER_BUILD ${vtkAddon_DIR}/<CMAKE_CFG_INTDIR>)
  mark_as_superbuild(
    VARS ${proj}_LIBRARY_PATHS_LAUNCHER_BUILD
    LABELS "LIBRARY_PATHS_LAUNCHER_BUILD"
  )
  # Add pythonpath to SlicerLauncherSettings.ini
  set(${proj}_PYTHONPATH_LAUNCHER_BUILD ${vtkAddon_DIR}/<CMAKE_CFG_INTDIR>)
  mark_as_superbuild(
    VARS ${proj}_PYTHONPATH_LAUNCHER_BUILD
    LABELS "PYTHONPATH_LAUNCHER_BUILD"
  )

  #-----------------------------------------------------------------------------
  # Launcher setting specific to install tree

  # pythonpath
  if(UNIX)
    set(${proj}_PYTHONPATH_LAUNCHER_INSTALLED
      <APPLAUNCHER_SETTINGS_DIR>/../lib/python${Slicer_REQUIRED_PYTHON_VERSION_DOT}/vtkAddon
      )
  else()
    set(${proj}_PYTHONPATH_LAUNCHER_INSTALLED
      <APPLAUNCHER_SETTINGS_DIR>/../lib/vtkAddon
      )
  endif()
  mark_as_superbuild(
    VARS ${proj}_PYTHONPATH_LAUNCHER_INSTALLED
    LABELS "PYTHONPATH_LAUNCHER_INSTALLED"
    )

else()
  ExternalProject_Add_Empty(${proj} DEPENDS ${${proj}_DEPENDENCIES})
endif()

mark_as_superbuild(
  VARS vtkAddon_DIR:PATH
  LABELS "FIND_PACKAGE"
)
