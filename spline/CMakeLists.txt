cmake_minimum_required(VERSION 3.21)
project(spline)

set(CMAKE_CXX_STANDARD 14)

add_executable(spline main.cpp src/smath.h src/smath.cpp src/spline.h src/spline.cpp)
