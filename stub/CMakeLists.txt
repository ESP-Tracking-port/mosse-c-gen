cmake_minimum_required(VERSION 2.8)
set(CMAKE_CXX_STANDARD 11)
project(mossetablestest)
file(GLOB SOURCES "*.cpp")
include_directories(".")
add_executable(mossetablestestcompile ${SOURCES})
