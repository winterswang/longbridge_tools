import pytest
import os
from longbridge_tools.quote import QuoteSkill
from longbridge_tools.trade import TradeSkill
from longbridge_tools.asset import AssetSkill
from longbridge_tools.config import AppConfig

@pytest.mark.skipif(not os.getenv("LONGBRIDGE_APP_KEY"), reason="No Longbridge credentials found")
def test_quote_integration():
    """
    Test QuoteSkill against real API.
    Requires environment variables: LONGBRIDGE_APP_KEY, LONGBRIDGE_APP_SECRET, LONGBRIDGE_ACCESS_TOKEN
    """
    config = AppConfig.from_env()
    skill = QuoteSkill(config)
    
    # Test real-time quote for Tencent (700.HK)
    # Note: Market data might be delayed or unavailable outside trading hours, but API call should succeed.
    try:
        quotes = skill.get_quote(["700.HK"])
        assert len(quotes) > 0
        assert quotes[0].symbol == "700.HK"
        print(f"Quote for 700.HK: {quotes[0]}")
    except Exception as e:
        pytest.fail(f"Failed to get quote: {e}")

@pytest.mark.skipif(not os.getenv("LONGBRIDGE_APP_KEY"), reason="No Longbridge credentials found")
def test_asset_integration():
    """
    Test AssetSkill against real API.
    """
    config = AppConfig.from_env()
    skill = AssetSkill(config)
    
    try:
        # Get account balance
        # Note: Depending on account type, might return multiple currencies
        balance = skill.get_account_balance()
        assert balance is not None
        print(f"Account Balance: {balance}")
    except Exception as e:
        pytest.fail(f"Failed to get asset info: {e}")

@pytest.mark.skipif(not os.getenv("LONGBRIDGE_APP_KEY"), reason="No Longbridge credentials found")
def test_trade_integration():
    """
    Test TradeSkill against real API.
    WARNING: This test places a limit order far from market price to avoid execution, 
    but use with caution. Ideally use a paper trading environment if available.
    """
    # Skipping actual order placement in automated tests to avoid unintended trades.
    # But we can query orders.
    config = AppConfig.from_env()
    skill = TradeSkill(config)
    
    try:
        orders = skill.get_orders()
        assert isinstance(orders, list)
        print(f"Today's Orders: {len(orders)}")
    except Exception as e:
        pytest.fail(f"Failed to get orders: {e}")
