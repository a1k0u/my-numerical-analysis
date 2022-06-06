cmake_minimum_required(VERSION 3.21)
project(spline)

set(CMAKE_CXX_STANDARD 14)

add_executable(spline
        main.cpp spline.cpp spline.h)
