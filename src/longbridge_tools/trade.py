from typing import List, Optional
from longport.openapi import TradeContext, Config, OrderType, OrderSide, TimeInForceType
from longbridge_tools.config import AppConfig

class TradeSkill:
    """
    Skill for interacting with Longbridge Trade API.
    Provides methods to place orders, cancel orders, and query order status.
    """
    
    def __init__(self, config: Optional[AppConfig] = None):
        if config is None:
            config = AppConfig.load()
        
        lp_config = Config(
            app_key=config.app_key,
            app_secret=config.app_secret,
            access_token=config.access_token
        )
        self.ctx = TradeContext(lp_config)

    def submit_order(self, symbol: str, side: str, order_type: str, quantity: int, price: float = None):
        """
        Submit a new order.
        
        Args:
            symbol: Stock symbol (e.g., "700.HK")
            side: "Buy" or "Sell"
            order_type: "LO" (Limit), "MO" (Market), etc.
            quantity: Order quantity
            price: Order price (required for Limit orders)
            
        Returns:
            Order submission result (order_id)
        """
        side_map = {
            "buy": OrderSide.Buy,
            "sell": OrderSide.Sell
        }
        
        type_map = {
            "lo": OrderType.LO,
            "mo": OrderType.MO,
        }
        
        return self.ctx.submit_order(
            symbol=symbol,
            order_type=type_map.get(order_type.lower(), OrderType.LO),
            side=side_map.get(side.lower(), OrderSide.Buy),
            submitted_quantity=quantity,
            submitted_price=price,
            time_in_force=TimeInForceType.Day
        )

    def cancel_order(self, order_id: str):
        """
        Cancel an existing order.
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            Cancellation result
        """
        return self.ctx.cancel_order(order_id)

    def get_orders(self, symbol: str = None):
        """
        Get today's orders.
        
        Args:
            symbol: Filter by symbol (optional)
            
        Returns:
            List of orders
        """
        return self.ctx.today_orders(symbol=symbol)

    def get_history_orders(self, symbol: str = None, start: str = None, end: str = None):
        """
        Get historical orders.
        
        Args:
            symbol: Filter by symbol (optional)
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD)
            
        Returns:
            List of historical orders
        """
        # Assuming history_orders method exists or similar
        return self.ctx.history_orders(symbol=symbol, start=start, end=end)
