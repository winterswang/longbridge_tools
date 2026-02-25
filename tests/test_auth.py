import pytest
import yaml
import requests
from unittest.mock import MagicMock
from longbridge_tools.auth import AuthSkill
from longbridge_tools.config import AppConfig

@pytest.fixture
def mock_config():
    return AppConfig(
        app_key="mock_key",
        app_secret="mock_secret",
        access_token="mock_token",
        http_url="https://mock.api"
    )

def test_refresh_token_success(mock_config, requests_mock):
    skill = AuthSkill(mock_config)
    expired_at = "2023-04-14T12:13:57.859Z"
    
    # Mock API response
    requests_mock.get(
        "https://mock.api/v1/token/refresh",
        json={
            "code": 0,
            "msg": "success",
            "data": {
                "token": "new_mock_token",
                "expired_at": "2023-05-14T12:13:57.859Z"
            }
        },
        status_code=200
    )
    
    result = skill.refresh_token(expired_at)
    
    assert result["token"] == "new_mock_token"
    assert requests_mock.called
    assert requests_mock.last_request.qs["expired_at"] == [expired_at] or \
           requests_mock.last_request.qs["expired_at"] == [expired_at.lower()] or \
           requests_mock.last_request.qs["expired_at"] == [requests.utils.unquote(expired_at)]
    assert requests_mock.last_request.headers["Authorization"] == "mock_token"

def test_refresh_token_api_error(mock_config, requests_mock):
    skill = AuthSkill(mock_config)
    
    requests_mock.get(
        "https://mock.api/v1/token/refresh",
        json={"code": 1001, "msg": "Invalid token", "data": {}},
        status_code=200
    )
    
    with pytest.raises(Exception, match="Longbridge API Error: Invalid token"):
        skill.refresh_token("any_date")

def test_refresh_token_network_error(mock_config, requests_mock):
    skill = AuthSkill(mock_config)
    
    requests_mock.get(
        "https://mock.api/v1/token/refresh",
        status_code=500
    )
    
    with pytest.raises(Exception, match="Network error"):
        skill.refresh_token("any_date")

def test_update_config_file(tmp_path):
    # Create a dummy config file
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump({"access_token": "old_token", "app_key": "k"}, f)
        
    skill = AuthSkill(AppConfig(app_key="k", app_secret="s", access_token="t"))
    
    skill.update_config_file("new_token", str(config_path))
    
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
        assert data["access_token"] == "new_token"
        assert data["app_key"] == "k"
