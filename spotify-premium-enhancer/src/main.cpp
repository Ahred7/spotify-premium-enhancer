#include <iostream>
#include "network/spotify_api.h"
#include "utils/logger.h"

int main() {
    Logger::log("Starting Spotify Premium Enhancer...");

    SpotifyAPI api;
    if (api.unlockPremium()) {
        Logger::log("Premium features unlocked successfully!");
    } else {
        Logger::log("Failed to unlock premium features.");
    }

    return 0;
}