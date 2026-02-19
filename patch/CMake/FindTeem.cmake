find_package(Teem REQUIRED CONFIG)
set_target_properties(teem PROPERTIES INTERFACE_INCLUDE_DIRECTORIES $<BUILD_INTERFACE:${Teem_INCLUDE_DIRS}>)
add_library(Teem::teem ALIAS teem)
