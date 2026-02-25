import pytest
import yaml
import os
from pathlib import Path
from longbridge_tools.config import AppConfig

@pytest.fixture
def config_file(tmp_path):
    """Create a temporary config file."""
    config_data = {
        "app_key": "file_key",
        "app_secret": "file_secret",
        "access_token": "file_token",
        "http_url": "https://custom.url"
    }
    path = tmp_path / "config.yaml"
    with open(path, "w") as f:
        yaml.dump(config_data, f)
    return path

def test_load_from_path(config_file):
    """Test loading from a specific file path."""
    config = AppConfig.load(config_file)
    assert config.app_key == "file_key"
    assert config.app_secret == "file_secret"
    assert config.access_token == "file_token"
    assert config.http_url == "https://custom.url"

def test_load_default_config_yaml(config_file, monkeypatch):
    """Test loading from default config.yaml in current directory."""
    # Change CWD to the directory containing the temporary config.yaml
    monkeypatch.chdir(config_file.parent)
    
    # Load without arguments, should pick up config.yaml
    config = AppConfig.load()
    assert config.app_key == "file_key"

def test_load_from_env(tmp_path, monkeypatch):
    """Test loading from environment variables when no file exists."""
    # Set env vars
    monkeypatch.setenv("LONGBRIDGE_APP_KEY", "env_key")
    monkeypatch.setenv("LONGBRIDGE_APP_SECRET", "env_secret")
    monkeypatch.setenv("LONGBRIDGE_ACCESS_TOKEN", "env_token")
    
    # Change to an empty directory to ensure no config.yaml exists
    monkeypatch.chdir(tmp_path)
    
    config = AppConfig.load()
    assert config.app_key == "env_key"
    assert config.app_secret == "env_secret"

def test_file_not_found():
    """Test explicitly provided path not found."""
    with pytest.raises(FileNotFoundError):
        AppConfig.load("non_existent_config.yaml")

def test_missing_fields(tmp_path):
    """Test validation of missing fields."""
    path = tmp_path / "bad_config.yaml"
    with open(path, "w") as f:
        yaml.dump({"app_key": "k"}, f)
        
    with pytest.raises(ValueError, match="Missing required configuration fields"):
        AppConfig.load(path)
