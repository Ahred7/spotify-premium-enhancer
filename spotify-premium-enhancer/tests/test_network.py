import pytest
from unittest.mock import patch, MagicMock
from src.network import SpotifyNetworkInterceptor

class TestSpotifyNetworkInterceptor:
    @pytest.fixture
    def interceptor(self):
        return SpotifyNetworkInterceptor()

    def test_redirect_premium_endpoint(self, interceptor):
        url = "https://api.spotify.com/v1/me/premium"
        redirected = interceptor.redirect_to_premium(url)
        assert redirected is not None
        assert "127.0.0.1:8888" in redirected

    def test_no_redirect_normal_endpoint(self, interceptor):
        url = "https://api.spotify.com/v1/me/playlists"
        redirected = interceptor.redirect_to_premium(url)
        assert redirected is None

    def test_mock_premium_response(self, interceptor):
        response = interceptor.mock_premium_response()
        assert response["premium"] == True
        assert response["product"] == "premium"
        assert response["subscription"]["valid_until"] == "2099-12-31T23:59:59Z"

    @patch('src.network.socket.create_connection')
    def test_health_check_success(self, mock_connection, interceptor):
        mock_connection.return_value = MagicMock()
        assert interceptor.health_check() == True

    @patch('src.network.socket.create_connection')
    def test_health_check_failure(self, mock_connection, interceptor):
        mock_connection.side_effect = ConnectionRefusedError
        assert interceptor.health_check() == False

    def test_intercept_request_redirects(self, interceptor, mocker):
        mock_session = mocker.patch.object(interceptor, 'session')
        mock_response = MagicMock()
        mock_session.request.return_value = mock_response
        
        url = "https://api.spotify.com/v1/me/premium"
        response = interceptor.intercept_request("GET", url)
        assert response == mock_response
        mock_session.request.assert_called_once()
        args, _ = mock_session.request.call_args
        assert "127.0.0.1:8888" in args[1]