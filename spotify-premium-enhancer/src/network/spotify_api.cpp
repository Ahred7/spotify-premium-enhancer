#include "spotify_api.h"
#include "../utils/logger.h"
#include <curl/curl.h>

size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

bool SpotifyAPI::unlockPremium() {
    CURL* curl = curl_easy_init();
    if (!curl) {
        Logger::log("Failed to initialize CURL");
        return false;
    }

    std::string readBuffer;
    curl_easy_setopt(curl, CURLOPT_URL, "https://api.spotify.com/v1/me");
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, nullptr); // Placeholder for auth headers

    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK) {
        Logger::log("CURL request failed: " + std::string(curl_easy_strerror(res)));
        return false;
    }

    Logger::log("API response: " + readBuffer);
    return true;
}