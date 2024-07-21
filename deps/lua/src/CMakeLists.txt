cmake_minimum_required(VERSION 3.10)
project(lua_static_lib C)

set(LIB_SRC
    fpconv.c  lapi.c  lauxlib.c  lbaselib.c  lcode.c  ldblib.c  ldebug.c  ldo.c  ldump.c  
    lfunc.c  lgc.c  linit.c  liolib.c  llex.c  lmathlib.c  lmem.c  loadlib.c  lobject.c  
    lopcodes.c  loslib.c  lparser.c  lstate.c  lstring.c  lstrlib.c  ltable.c  ltablib.c  
    ltm.c  lua.c  luac.c  lua_bit.c  lua_cjson.c  lua_cmsgpack.c  lua_struct.c  lundump.c  
    lvm.c  lzio.c  print.c  strbuf.c
)

# Specify include directories
include_directories(
    ${CMAKE_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/../deps
    ${CMAKE_SOURCE_DIR}/../deps/hiredis
    ${CMAKE_SOURCE_DIR}/../deps/linenoise
    ${CMAKE_SOURCE_DIR}/../deps/lua/src
    ${CMAKE_SOURCE_DIR}/../deps/hdr_histogram
    ${CMAKE_SOURCE_DIR}/../deps/jemalloc/src
)

# Create the static library
add_library(lua_static STATIC ${LIB_SRC})

# Platform-specific settings (examples, add more if needed)
if(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    add_definitions(-DLUA_USE_LINUX)
    target_link_libraries(lua_static m dl)
elseif(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    add_definitions(-DLUA_USE_MACOSX)
    target_link_libraries(lua_static m dl)
elseif(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    add_definitions(-DLUA_USE_WINDOWS)
    target_link_libraries(lua_static ws2_32)
endif()
