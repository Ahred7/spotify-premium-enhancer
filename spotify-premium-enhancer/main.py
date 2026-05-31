#!/usr/bin/env python3
"""Spotify Premium Enhancer - Main Entry Point"""

import sys
import logging
from src.core import SpotifyPremiumEnhancer
from src.network import SpotifyNetworkInterceptor

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("spotify_enhancer.log")
        ]
    )

def main():
    setup_logging()
    logger = logging.getLogger("main")

    logger.info("Starting Spotify Premium Enhancer v1.0.0")

    enhancer = SpotifyPremiumEnhancer()
    interceptor = SpotifyNetworkInterceptor()

    # Attempt unlock
    if enhancer.unlock_premium():
        logger.info("Premium unlock successful")
        patches = enhancer.apply_patches()
        logger.info(f"Applied patches: {patches}")
    else:
        logger.warning("Premium unlock failed - check config")

    # Test network interceptor
    test_url = "https://api.spotify.com/v1/me/premium"
    logger.info(f"Testing interceptor with: {test_url}")
    redirected = interceptor.redirect_to_premium(test_url)
    if redirected:
        logger.info(f"Would redirect to: {redirected}")

    # Print status
    status = enhancer.status()
    logger.info(f"Status: active={status['active']}")

    print("Spotify Premium Enhancer running. Check spotify_enhancer.log for details.")

if __name__ == "__main__":
    main()