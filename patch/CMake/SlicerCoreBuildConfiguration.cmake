# Select build flags for release mode
if(CMAKE_CXX_COMPILER_FRONTEND_VARIANT STREQUAL "GNU")
  # use -O2 rather than -O3 as the wheel gets significantly larger in -O3 for no real benefit.
  set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
endif()

# Select a better linker when available.
# This was made due to vtkITK being rather slow to link with LD.
# But it isn't a hard requirement.
if(UNIX AND CMAKE_VERSION VERSION_GREATER_EQUAL 3.29 OR NOT USE_SYSTEM_LINKER)
  # Try to used mold first
  if((CMAKE_CXX_COMPILER_ID STREQUAL "GNU"
    AND CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 12.1)
    OR CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    find_program(MOLD_LINKER mold)

    if(MOLD_LINKER)
      message(STATUS "Using linker mold")
      set(CMAKE_LINKER_TYPE MOLD)
      return()
    endif()
  endif()

  # Try to used lld if mold can not be used
  if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    find_program(LLD_LINKER lld)

    if(LLD_LINKER)
      message(STATUS "Using linker lld")
      set(CMAKE_LINKER_TYPE LLD)
      return()
    endif()
  endif()
endif()
