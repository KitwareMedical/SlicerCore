cmake_minimum_required(VERSION 3.17...4.0)

project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

# As long as the find package does not fail, it won't be shown by pytest
set(CMAKE_FIND_DEBUG_MODE TRUE)
find_package(Slicer CONFIG REQUIRED)
set(CMAKE_FIND_DEBUG_MODE FALSE)
