cmake_minimum_required(VERSION 3.10)
project(spotify_premium_enhancer)

set(CMAKE_CXX_STANDARD 17)

add_executable(spotify-premium-enhancer
    src/main.cpp
    src/network/spotify_api.cpp
    src/utils/logger.cpp
)

target_include_directories(spotify-premium-enhancer PRIVATE src)
target_link_libraries(spotify-premium-enhancer PRIVATE curl)