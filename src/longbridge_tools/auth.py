import requests
import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from longbridge_tools.config import AppConfig

class AuthSkill:
    """
    Skill for authentication management, including token refresh.
    """
    
    def __init__(self, config: Optional[AppConfig] = None):
        if config is None:
            self.config = AppConfig.load()
        else:
            self.config = config

    def refresh_token(self, expired_at: str) -> Dict[str, Any]:
        """
        Refresh the access token.
        
        Args:
            expired_at: The expiration time of the current token (ISO8601 format).
                       e.g. "2023-04-14T12:13:57.859Z"
            
        Returns:
            Dict containing the new token info.
        """
        # Note: The API requires 'expired_at' parameter in GET request
        # The endpoint is /v1/token/refresh
        
        # Ensure http_url is correct (remove trailing slash if any)
        base_url = self.config.http_url.rstrip("/")
        url = f"{base_url}/v1/token/refresh"
        
        headers = {
            "Authorization": self.config.access_token,
            # 'Content-Type': 'application/json' # GET request doesn't need content-type usually but harmless
        }
        
        params = {
            "expired_at": expired_at
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") != 0:
                raise Exception(f"Longbridge API Error: {result.get('msg')} (Code: {result.get('code')})")
                
            return result["data"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error during token refresh: {e}")

    def update_config_file(self, new_token: str, config_path: str = "config.yaml") -> None:
        """
        Update the configuration file with the new access token.
        Preserves comments is hard with standard yaml, so this might overwrite comments.
        To preserve comments, we'd need a round-trip loader like ruamel.yaml, 
        but for now standard yaml dump is used as per dependencies.
        
        Args:
            new_token: The new access token.
            config_path: Path to the config file.
        """
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            
        config_data["access_token"] = new_token
        
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f, sort_keys=False, allow_unicode=True)

