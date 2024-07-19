cmake_minimum_required(VERSION 3.10)
project(redis)

# CMake variables
set(PROG_SUFFIX "")

find_package(Threads REQUIRED)

# Executable names
set(REDIS_SERVER_NAME redis-server${PROG_SUFFIX})
set(REDIS_SENTINEL_NAME redis-sentinel${PROG_SUFFIX})
set(REDIS_CLI_NAME redis-cli${PROG_SUFFIX})
set(REDIS_BENCHMARK_NAME redis-benchmark${PROG_SUFFIX})
set(REDIS_CHECK_RDB_NAME redis-check-rdb${PROG_SUFFIX})
set(REDIS_CHECK_AOF_NAME redis-check-aof${PROG_SUFFIX})

set(MKRELEASEHDR_PATH ${CMAKE_SOURCE_DIR}/mkreleasehdr.sh)

execute_process(
    COMMAND sh -c ${MKRELEASEHDR_PATH}
    OUTPUT_VARIABLE RELEASE_HDR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Source files
set(REDIS_SERVER_OBJ
    adlist.c quicklist.c ae.c anet.c dict.c server.c sds.c zmalloc.c lzf_c.c lzf_d.c pqsort.c zipmap.c sha1.c ziplist.c release.c networking.c util.c object.c db.c replication.c rdb.c t_string.c t_list.c t_set.c t_zset.c t_hash.c config.c aof.c pubsub.c multi.c debug.c sort.c intset.c syncio.c cluster.c crc16.c endianconv.c slowlog.c eval.c bio.c rio.c rand.c memtest.c syscheck.c crcspeed.c crc64.c bitops.c sentinel.c notify.c setproctitle.c blocked.c hyperloglog.c latency.c sparkline.c redis-check-rdb.c redis-check-aof.c geo.c lazyfree.c module.c evict.c expire.c geohash.c geohash_helper.c childinfo.c defrag.c siphash.c rax.c t_stream.c listpack.c localtime.c lolwut.c lolwut5.c lolwut6.c acl.c tracking.c connection.c tls.c sha256.c timeout.c setcpuaffinity.c monotonic.c mt19937-64.c resp_parser.c call_reply.c script_lua.c script.c functions.c function_lua.c commands.c
)

set(REDIS_CLI_OBJ
    anet.c adlist.c dict.c redis-cli.c zmalloc.c release.c ae.c redisassert.c crcspeed.c crc64.c siphash.c crc16.c monotonic.c cli_common.c mt19937-64.c
)

set(REDIS_BENCHMARK_OBJ
    ae.c anet.c redis-benchmark.c adlist.c dict.c zmalloc.c redisassert.c release.c crcspeed.c crc64.c siphash.c crc16.c monotonic.c cli_common.c mt19937-64.c
)

# Include directories
include_directories(
    ${CMAKE_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/../deps
    ${CMAKE_SOURCE_DIR}/../deps/hiredis
    ${CMAKE_SOURCE_DIR}/../deps/linenoise
    ${CMAKE_SOURCE_DIR}/../deps/lua/src
    ${CMAKE_SOURCE_DIR}/../deps/hdr_histogram
    ${CMAKE_SOURCE_DIR}/../deps/jemalloc/src)


# Set compiler flags
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -W -Wno-missing-field-initializers")

# Add executables
add_executable(${REDIS_SERVER_NAME} ${REDIS_SERVER_OBJ})
add_executable(${REDIS_CLI_NAME} ${REDIS_CLI_OBJ})
add_executable(${REDIS_BENCHMARK_NAME} ${REDIS_BENCHMARK_OBJ})
add_executable(${REDIS_SENTINEL_NAME} EXCLUDE_FROM_ALL ${REDIS_SERVER_OBJ})
add_executable(${REDIS_CHECK_RDB_NAME} EXCLUDE_FROM_ALL ${REDIS_SERVER_OBJ})
add_executable(${REDIS_CHECK_AOF_NAME} EXCLUDE_FROM_ALL ${REDIS_SERVER_OBJ})

# Link libraries (assuming libraries are pre-built and paths are correct)
target_link_libraries(${REDIS_SERVER_NAME} PRIVATE hiredis lua hdr_histogram pthread)
target_link_libraries(${REDIS_CLI_NAME} PRIVATE hiredis linenoise pthread)
target_link_libraries(${REDIS_BENCHMARK_NAME} PRIVATE hiredis hdr_histogram pthread)

# Custom commands to handle post-build tasks
add_custom_command(TARGET ${REDIS_SENTINEL_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${REDIS_SERVER_NAME}> $<TARGET_FILE:${REDIS_SENTINEL_NAME}>
)

add_custom_command(TARGET ${REDIS_CHECK_RDB_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${REDIS_SERVER_NAME}> $<TARGET_FILE:${REDIS_CHECK_RDB_NAME}>
)

add_custom_command(TARGET ${REDIS_CHECK_AOF_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${REDIS_SERVER_NAME}> $<TARGET_FILE:${REDIS_CHECK_AOF_NAME}>
)

# Install rules
install(TARGETS ${REDIS_SERVER_NAME} ${REDIS_CLI_NAME} ${REDIS_BENCHMARK_NAME}
    RUNTIME DESTINATION bin
)

install(FILES $<TARGET_FILE:${REDIS_SERVER_NAME}>
    DESTINATION bin
    RENAME ${REDIS_SENTINEL_NAME}
)

install(FILES $<TARGET_FILE:${REDIS_SERVER_NAME}>
    DESTINATION bin
    RENAME ${REDIS_CHECK_RDB_NAME}
)

install(FILES $<TARGET_FILE:${REDIS_SERVER_NAME}>
    DESTINATION bin
    RENAME ${REDIS_CHECK_AOF_NAME}
)

# Custom target to persist settings (using dummy commands as placeholders)
add_custom_target(persist-settings ALL
    COMMAND echo "Persisting settings..."
)

add_dependencies(${REDIS_SERVER_NAME} persist-settings)
add_dependencies(${REDIS_CLI_NAME} persist-settings)
add_dependencies(${REDIS_BENCHMARK_NAME} persist-settings)

# Custom target for clean and distclean
add_custom_target(clean-all
    COMMAND ${CMAKE_COMMAND} --build . --target clean
    COMMAND rm -rf *.gcda *.gcno *.gcov redis.info lcov-html Makefile.dep
)

add_custom_target(distclean
    COMMAND ${CMAKE_COMMAND} --build . --target clean-all
    COMMAND rm -rf .make-*
)
