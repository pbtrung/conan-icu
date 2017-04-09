project(tst_icu)
cmake_minimum_required(VERSION 2.8.12)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(tst_icu icu.cpp)
target_link_libraries(tst_icu ${CONAN_LIBS})
