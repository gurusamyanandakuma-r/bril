cmake_minimum_required(VERSION 3.13.4)
project(DivCheckPass)

find_package(LLVM 10.0 REQUIRED CONFIG)
message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")

include_directories(${LLVM_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})

add_library(DivCheckPass MODULE
    DivCheckPass.cpp
)

# Use C++11
target_compile_features(DivCheckPass PRIVATE cxx_range_for cxx_auto_type)

# Set proper shared library suffix
if(APPLE)
    set_target_properties(DivCheckPass PROPERTIES
        LINK_FLAGS "-undefined dynamic_lookup"
        SUFFIX ".dylib")
elseif(UNIX)
    set_target_properties(DivCheckPass PROPERTIES
        PREFIX ""
        SUFFIX ".so")
endif()