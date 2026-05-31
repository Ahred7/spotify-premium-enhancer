import pytest
import json
import tempfile
from pathlib import Path
from src.core import SpotifyPremiumEnhancer

class TestSpotifyPremiumEnhancer:
    @pytest.fixture
    def enhancer(self, tmp_path):
        config_file = tmp_path / "test_config.json"
        config = {
            "enabled": True,
            "skip_ads": True,
            "unlimited_skips": True,
            "high_quality": True,
            "offline_mode": False
        }
        with open(config_file, 'w') as f:
            json.dump(config, f)
        return SpotifyPremiumEnhancer(config_path=str(config_file))

    def test_initial_state(self, enhancer):
        assert enhancer.is_active == False
        assert enhancer.config["enabled"] == True

    def test_unlock_premium_success(self, enhancer):
        result = enhancer.unlock_premium()
        assert result == True
        assert enhancer.is_active == True

    def test_unlock_premium_disabled(self, enhancer):
        enhancer.config["enabled"] = False
        result = enhancer.unlock_premium()
        assert result == False
        assert enhancer.is_active == False

    def test_apply_patches(self, enhancer):
        patches = enhancer.apply_patches()
        assert patches["ad_blocker"] == True
        assert patches["skip_limit"] == True
        assert patches["audio_quality"] == "high"
        assert patches["offline_access"] == False

    def test_toggle(self, enhancer):
        assert enhancer.is_active == False
        enhancer.toggle()
        assert enhancer.is_active == True
        enhancer.toggle()
        assert enhancer.is_active == False

    def test_status(self, enhancer):
        status = enhancer.status()
        assert "active" in status
        assert "config" in status
        assert "patches" in status
        assert status["active"] == False

    def test_config_creation(self, tmp_path):
        config_path = str(tmp_path / "new_config.json")
        enhancer = SpotifyPremiumEnhancer(config_path=config_path)
        assert Path(config_path).exists()
        with open(config_path) as f:
            config = json.load(f)
        assert config["enabled"] == True