import pytest
import os
from unittest.mock import MagicMock
from longbridge_tools.config import AppConfig

@pytest.fixture
def mock_config():
    return AppConfig(
        app_key="mock_key",
        app_secret="mock_secret",
        access_token="mock_token"
    )

@pytest.fixture
def mock_quote_context(mocker):
    mock = mocker.patch("longbridge_tools.quote.QuoteContext")
    return mock.return_value

@pytest.fixture
def mock_trade_context(mocker):
    mock = mocker.patch("longbridge_tools.trade.TradeContext")
    return mock.return_value

@pytest.fixture
def mock_asset_context(mocker):
    # AssetSkill uses TradeContext
    mock = mocker.patch("longbridge_tools.asset.TradeContext")
    return mock.return_value
