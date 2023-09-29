cmake_minimum_required(VERSION 3.22.1)
project(ztime VERSION 0.1 DESCRIPTION "GUI application to track time spent on things.")

file(GLOB_RECURSE SOURCE_FILES ${CMAKE_SOURCE_DIR}/src/*.c ${CMAKE_SOURCE_DIR}/src/*.cpp)
file(GLOB_RECURSE HEADER_FILES ${CMAKE_SOURCE_DIR}/src/*.h ${CMAKE_SOURCE_DIR}/src/*.hpp)

find_package(OpenGL REQUIRED)
find_package(glm REQUIRED)
find_package(assimp REQUIRED)
find_package(glfw3 3.3 REQUIRED)

link_directories(${GLFW3_LIB_PATH})
set(LIBS glfw glm::glm assimp openal z m ogg vorbis vorbisfile freetype)
include_directories(
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/third-party/
    /mnt/Code/c++/_lib/gl/include/
    /mnt/Code/c++/_lib/al/include/
    /mnt/Code/c++/nbt/
    /mnt/Code/c++/_lib/rapidxml-1.13/
)

add_compile_definitions(_SILENCE_CXX17_CODECVT_HEADER_DEPRECATION_WARNING)
add_executable(${PROJECT_NAME} ${HEADER_FILES} ${CMAKE_SOURCE_DIR}/third-party/glad.c ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${LIBS})

target_compile_options(${PROJECT_NAME} PUBLIC "$<$<CONFIG:Debug>:-DDEBUG;-g;-Wall>")
target_compile_options(${PROJECT_NAME} PUBLIC "$<$<CONFIG:Release>:-O3>")