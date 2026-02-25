from typing import List, Optional
from longport.openapi import QuoteContext, Config
from longbridge_tools.config import AppConfig

class QuoteSkill:
    """
    Skill for interacting with Longbridge Quote API.
    Provides methods to fetch real-time and historical market data.
    """
    
    def __init__(self, config: Optional[AppConfig] = None):
        if config is None:
            config = AppConfig.load()
        
        lp_config = Config(
            app_key=config.app_key,
            app_secret=config.app_secret,
            access_token=config.access_token
        )
        self.ctx = QuoteContext(lp_config)

    def get_quote(self, symbols: List[str]):
        """
        Get real-time quote for symbols.
        
        Args:
            symbols: List of stock symbols (e.g., ["700.HK", "AAPL.US"])
            
        Returns:
            List of Quote objects
        """
        return self.ctx.quote(symbols)

    def get_depth(self, symbol: str):
        """
        Get market depth (order book) for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Depth object
        """
        return self.ctx.depth(symbol)

    def get_brokers(self, symbol: str):
        """
        Get broker queue for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Brokers object
        """
        return self.ctx.brokers(symbol)
    
    def get_candlesticks(self, symbol: str, period: str, count: int, adjust_type: str = "no_adjust"):
        """
        Get historical candlesticks.
        
        Args:
            symbol: Stock symbol
            period: Period (e.g., "day", "min_1", "min_5")
            count: Number of candlesticks
            adjust_type: Adjustment type ("no_adjust", "forward_adjust")
            
        Returns:
            List of Candlestick objects
        """
        # Mapping period string to longport enum if needed, but longport often takes strings or enums.
        # Assuming longport SDK handles string/enum conversion or we pass proper Period enum.
        from longport.openapi import Period, AdjustType
        
        p_map = {
            "day": Period.Day,
            "week": Period.Week,
            "month": Period.Month,
            "year": Period.Year,
            "min_1": Period.Min_1,
            "min_5": Period.Min_5,
        }
        
        a_map = {
            "no_adjust": AdjustType.NoAdjust,
            "forward_adjust": AdjustType.ForwardAdjust,
        }
        
        return self.ctx.candlesticks(symbol, p_map.get(period, Period.Day), count, a_map.get(adjust_type, AdjustType.NoAdjust))

    def get_watchlist(self):
        """
        Get all watchlist groups and securities.
        
        Returns:
            List of WatchlistGroup objects
        """
        return self.ctx.watchlist()
