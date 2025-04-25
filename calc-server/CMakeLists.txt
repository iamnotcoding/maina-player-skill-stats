cmake_minimum_required(VERSION 3.5)

project(CALC_SERVER)

add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>") # force UTF-8 as the execution character set
add_executable(server "server.cpp" "socket_util.c")

set_property(TARGET server PROPERTY CXX_STANDARD 20)
# Typically you don't care so much for a third party library's tests to be
# run from your own project's code.
set(JSON_BuildTests OFF CACHE INTERNAL "")

# If you only include this third party in PRIVATE source files, you do not
# need to install it when your main project gets installed.
# set(JSON_Install OFF CACHE INTERNAL "")

# Don't use include(nlohmann_json/CMakeLists.txt) since that carries with it
# unintended consequences that will break the build.  It's generally
# discouraged (although not necessarily well documented as such) to use
# include(...) for pulling in other CMake projects anyways.
add_subdirectory(nlohmann_json)

target_link_libraries(server PRIVATE nlohmann_json::nlohmann_json)

target_link_libraries(server PRIVATE Ws2_32)