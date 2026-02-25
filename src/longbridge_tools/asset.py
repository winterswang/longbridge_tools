from typing import List, Optional
from longport.openapi import TradeContext, Config
from longbridge_tools.config import AppConfig

class AssetSkill:
    """
    Skill for interacting with Longbridge Asset API.
    Provides methods to query account balance, positions, and cash flow.
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

    def get_account_balance(self, currency: str = None):
        """
        Get account balance.
        
        Args:
            currency: Filter by currency (optional)
            
        Returns:
            Account balance details
        """
        # The method might be account_balance(currency=...) check docs/signature later
        # Assuming it takes optional args or returns all.
        return self.ctx.account_balance(currency=currency)

    def get_stock_positions(self, symbol: str = None):
        """
        Get stock positions.
        
        Args:
            symbol: Filter by symbol (optional)
            
        Returns:
            List of stock positions
        """
        return self.ctx.stock_positions(symbol=symbol)

    def get_cash_flow(self, start: str, end: str):
        """
        Get cash flow history.
        
        Args:
            start: Start date
            end: End date
            
        Returns:
            Cash flow records
        """
        return self.ctx.cash_flow(start=start, end=end)
