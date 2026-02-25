import os
import yaml
from dataclasses import dataclass
from typing import Optional, Dict, Any, Union
from pathlib import Path

@dataclass
class AppConfig:
    app_key: str
    app_secret: str
    access_token: str
    http_url: str = "https://openapi.lbkrs.com"
    quote_ws_url: str = "wss://openapi-quote.longbridge.global"
    trade_ws_url: str = "wss://openapi-trade.longbridge.global"

    @classmethod
    def load(cls, config_path: Optional[Union[str, Path]] = None) -> "AppConfig":
        """
        Load configuration.
        Priority:
        1. Specified config file path
        2. Default config file (config.yaml) in current directory
        3. Default config file (config.yaml) in parent directory
        4. Environment variables
        """
        # 1. Try specified path
        if config_path:
            path = Path(config_path)
            if path.exists():
                return cls.from_file(path)
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        # 2. Try default locations
        search_paths = [
            Path("config.yaml"),
            Path("../config.yaml"),
            Path(__file__).parent.parent.parent / "config.yaml"  # Project root (if in editable mode)
        ]
        
        for p in search_paths:
            if p.exists():
                return cls.from_file(p)

        # 3. Fallback to environment variables
        return cls.from_env()

    @classmethod
    def from_file(cls, file_path: Union[str, Path] = "config.yaml") -> "AppConfig":
        """
        Load configuration from a YAML file.
        
        Args:
            file_path: Path to the YAML configuration file.
            
        Returns:
            AppConfig object
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
            
        with open(path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            
        if not config_data:
            raise ValueError(f"Configuration file is empty: {file_path}")
            
        # Validate required fields
        required_fields = ["app_key", "app_secret", "access_token"]
        missing = [field for field in required_fields if field not in config_data]
        if missing:
            raise ValueError(f"Missing required configuration fields: {', '.join(missing)}")
            
        return cls(
            app_key=config_data["app_key"],
            app_secret=config_data["app_secret"],
            access_token=config_data["access_token"],
            http_url=config_data.get("http_url", "https://openapi.lbkrs.com"),
            quote_ws_url=config_data.get("quote_ws_url", "wss://openapi-quote.longbridge.global"),
            trade_ws_url=config_data.get("trade_ws_url", "wss://openapi-trade.longbridge.global")
        )

    @classmethod
    def from_env(cls) -> "AppConfig":
        """
        Load configuration from environment variables.
        """
        app_key = os.getenv("LONGBRIDGE_APP_KEY")
        app_secret = os.getenv("LONGBRIDGE_APP_SECRET")
        access_token = os.getenv("LONGBRIDGE_ACCESS_TOKEN")

        if not all([app_key, app_secret, access_token]):
            raise ValueError(
                "Missing required configuration. Please provide a config.yaml file "
                "or set LONGBRIDGE_APP_KEY, LONGBRIDGE_APP_SECRET, LONGBRIDGE_ACCESS_TOKEN environment variables."
            )

        return cls(
            app_key=app_key,
            app_secret=app_secret,
            access_token=access_token
        )
