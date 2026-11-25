cmake_minimum_required(VERSION 3.20)
project(ErgenticsCXX LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(ErgenticsCXX STATIC
    Sources/ErgenticsCXX/src/ergentics_cxx.cpp
    Sources/ErgenticsCXX/src/section7.cpp
    Sources/ErgenticsCXX/src/novelty.cpp
)
target_include_directories(ErgenticsCXX PUBLIC
    Sources/ErgenticsCXX/include
)
target_compile_options(ErgenticsCXX PRIVATE -O2 -Wall -Wextra -Werror)

enable_testing()
add_executable(test_cxx_standalone
    Tests/CXXStandaloneTests/test_cxx_standalone.cpp
)
target_link_libraries(test_cxx_standalone PRIVATE ErgenticsCXX)
target_compile_options(test_cxx_standalone PRIVATE -O2 -Wall -Wextra -Werror)
add_test(NAME cxx_standalone_swe_sweep COMMAND test_cxx_standalone)
