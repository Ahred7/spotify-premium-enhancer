#include "../src/network/spotify_api.h"
#include "../src/utils/logger.h"
#include <cassert>

void testUnlockPremium() {
    SpotifyAPI api;
    bool result = api.unlockPremium();
    assert(result == true); // Simplified for example
    Logger::log("Test passed: unlockPremium()");
}

int main() {
    testUnlockPremium();
    return 0;
}