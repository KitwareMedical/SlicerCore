cmake_minimum_required(VERSION 3.21...3.31)

project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

option(BUILD_SHARED_LIBS "Build shared libraries." ON)
option(BUILD_SDK "If ON, build SlicerCore-SDK instead of SlicerCore runtime" OFF)
option(USE_SUPERBUILD "Build dependencies using Slicer superbuild" ON)
option(USE_SYSTEM_LINKER "Slicer core uses mold or lld on Linux when available, if ON this will fallback to system linker" OFF)

list(PREPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMake")
include(SlicerCoreBuildConfiguration) # do some special configurations
include(SlicerCoreModuleWrapper)

# Superbuild
if(USE_SUPERBUILD)
  include(SlicerCoreSuperbuild)
  return()
endif()

if(BUILD_SDK AND (NOT DEFINED SDK_DEPS_DIR OR NOT EXISTS "${SDK_DEPS_DIR}"))
  message(FATAL_ERROR "SDK_DEPS_DIR must be defined to the location of ITK (and its dependencies) and vtkAddon install trees.")
endif()

set(modules
  # Libs/
  Slicer::ITK
  Slicer::RemoteIO
  Slicer::SegmentationCore
  Slicer::Teem
  # Libs/MRML
  Slicer::MRMLCLI
  Slicer::MRMLCore
  Slicer::MRMLDisplayableManager
  Slicer::MRMLLogic
  # Modules/Loadable
  Slicer::AnnotationsModuleLogic
  Slicer::AnnotationsModuleMRML
  Slicer::BaseLogic
  Slicer::CamerasModuleLogic
  Slicer::ColorsModuleLogic
  Slicer::ColorsModuleMRML
  Slicer::ColorsModuleMRMLDisplayableManager
  Slicer::ColorsModuleVTKWidgets
  Slicer::CropVolumeModuleLogic
  Slicer::CropVolumeModuleMRML
  Slicer::DataModuleLogic
  Slicer::MarkupsModuleLogic
  Slicer::MarkupsModuleMRML
  Slicer::MarkupsModuleMRMLDisplayableManager
  Slicer::MarkupsModuleVTKWidgets
  Slicer::ModelsModuleLogic
  Slicer::PlotsModuleLogic
  Slicer::ReformatModuleLogic
  Slicer::SceneViewsModuleLogic
  Slicer::SegmentationsModuleLogic
  Slicer::SegmentationsModuleMRML
  Slicer::SegmentationsModuleMRMLDisplayableManager
  Slicer::SequencesModuleLogic
  Slicer::SequencesModuleMRML
  Slicer::SubjectHierarchyModuleLogic
  Slicer::TablesModuleLogic
  Slicer::TerminologiesModuleLogic
  Slicer::TextsModuleLogic
  Slicer::TransformsModuleLogic
  Slicer::TransformsModuleMRMLDisplayableManager
  Slicer::UnitsModuleLogic
  Slicer::ViewControllersModuleLogic
  Slicer::VolumeRenderingModuleLogic
  Slicer::VolumeRenderingModuleMRML
  Slicer::VolumeRenderingModuleMRMLDisplayableManager
  Slicer::VolumesModuleLogic
)

set(layout Runtime)
if(BUILD_SDK)
  set(layout SDK)
endif()

include(VTKSDKPythonWheelHelper)

# Install runtime only dependencies
vtksdk_build_modules(${SKBUILD_PROJECT_NAME}
  MODULES ${modules}
  LAYOUT ${layout}
)

if(BUILD_SDK)
  vtksdk_install_modules_sdk(${SKBUILD_PROJECT_NAME}
    MODULES ${modules}
    PREFIX_PATHS
      "slicer_core_sdk/content/third_party"
    CMAKE_MODULES_INCLUDED
      "${CMAKE_CURRENT_SOURCE_DIR}/CMake/SlicerCoreModuleWrapper.cmake"
  )

  # Install dependencies required to consume SlicerCore as a SDK
  install(
    DIRECTORY ${SDK_DEPS_DIR}/
    DESTINATION slicer_core_sdk/content/third_party
    USE_SOURCE_PERMISSIONS
  )

  if(UNIX)
    # DCMTK do not use the right prefix for CMake scripts, this is a simple passthrough to make CMake happy
    install(
      DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/SlicerCoreSDK/third_party_patches/cmake/DCMTK/
      DESTINATION slicer_core_sdk/content/third_party/lib/cmake/DCMTK
    )
  endif()
else()
  vtksdk_generate_package_init(${SKBUILD_PROJECT_NAME} MODULES ${modules})
  vtksdk_install_runtimes_deps(${SKBUILD_PROJECT_NAME} MODULES ${modules})

  # These scripts enable users to use slicer in python as-if they were using SlicerPython
  # Example: `import slicer; slicer.vtkMRMLNode()`
  install(FILES
    ${CMAKE_SOURCE_DIR}/SlicerCore/Python/slicer/__init__.py
    ${CMAKE_SOURCE_DIR}/SlicerCore/Python/slicer/slicer_core.py
    DESTINATION slicer
  )

  # Install scripts from classic SlicerPython
  # Everything related to ctk, qt, etc is not supported,
  # so calling some function of util.py will fail at runtime.
  set(Slicer_PYTHON_SOURCE_DIR ${CMAKE_SOURCE_DIR}/Base/Python)
  install(FILES
    ${Slicer_PYTHON_SOURCE_DIR}/slicer/util.py
    DESTINATION slicer
  )
endif()
