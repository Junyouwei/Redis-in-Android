cmake_minimum_required(VERSION 3.10)
project(linenoise_library C)

# Set compiler flags
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Os -g")

# Include directories (if any)
include_directories(${CMAKE_SOURCE_DIR})

# Source files
set(SOURCE_FILES
    linenoise.c
    example.c
)

# Create the static library
add_library(linenoise STATIC ${SOURCE_FILES})

# Clean target (optional)
add_custom_target(clean-all
    COMMAND ${CMAKE_COMMAND} -E remove linenoise_static
    COMMAND ${CMAKE_COMMAND} -E remove_directory CMakeFiles
    COMMAND ${CMAKE_COMMAND} -E remove CMakeCache.txt cmake_install.cmake
)
