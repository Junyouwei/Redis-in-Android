cmake_minimum_required(VERSION 3.10)
project(hdrhistogram C)

# Set compiler flags
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -O2 -g -DANDROID -fdata-sections -ffunction-sections -funwind-tables -fstack-protector-strong -no-canonical-prefixes -D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security -fexceptions")

# Include directories
include_directories(${CMAKE_SOURCE_DIR})


# Source files
set(SOURCE_FILES
    hdr_histogram.c
)

# Create the static library
add_library(hdrhistogram STATIC ${SOURCE_FILES})

target_include_directories(hdrhistogram PRIVATE ${CMAKE_SOURCE_DIR})