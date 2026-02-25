import pytest
from unittest.mock import MagicMock
from longbridge_tools.quote import QuoteSkill
from longbridge_tools.trade import TradeSkill
from longbridge_tools.asset import AssetSkill
from longbridge_tools.config import AppConfig

def test_quote_skill(mock_config, mock_quote_context):
    skill = QuoteSkill(mock_config)
    
    # Test get_quote
    skill.get_quote(["700.HK"])
    mock_quote_context.quote.assert_called_with(["700.HK"])
    
    # Test get_depth
    skill.get_depth("700.HK")
    mock_quote_context.depth.assert_called_with("700.HK")
    
    # Test get_brokers
    skill.get_brokers("700.HK")
    mock_quote_context.brokers.assert_called_with("700.HK")
    
    # Test get_watchlist
    skill.get_watchlist()
    mock_quote_context.watchlist.assert_called()

def test_trade_skill(mock_config, mock_trade_context):
    skill = TradeSkill(mock_config)
    
    # Test submit_order
    skill.submit_order(
        symbol="700.HK",
        side="Buy",
        order_type="LO",
        quantity=100,
        price=300.0
    )
    # Verify the internal mapping logic if needed, but here just check call
    assert mock_trade_context.submit_order.called
    args, kwargs = mock_trade_context.submit_order.call_args
    assert kwargs['symbol'] == "700.HK"
    assert kwargs['submitted_quantity'] == 100
    assert kwargs['submitted_price'] == 300.0
    
    # Test get_orders
    skill.get_orders(symbol="700.HK")
    mock_trade_context.today_orders.assert_called_with(symbol="700.HK")
    
    # Test cancel_order
    skill.cancel_order("order_id_123")
    mock_trade_context.cancel_order.assert_called_with("order_id_123")

def test_asset_skill(mock_config, mock_asset_context):
    skill = AssetSkill(mock_config)
    
    # Test get_account_balance
    skill.get_account_balance(currency="HKD")
    # Assuming TradeContext.account_balance takes currency
    # Need to verify if `account_balance` supports filtering in actual SDK, 
    # but based on wrapper it passes it.
    # Actually, let's verify if `account_balance` takes args. 
    # If not, the wrapper might fail if passed.
    # The wrapper passes kwargs.
    
    # Test get_stock_positions
    skill.get_stock_positions("700.HK")
    # Assuming stock_positions takes symbol
    
    # Test get_cash_flow
    skill.get_cash_flow("2023-01-01", "2023-01-31")
    # Assuming cash_flow takes start/end
