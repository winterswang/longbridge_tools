from typing import List, Dict, Optional, Union
from decimal import Decimal
from longbridge_tools.config import AppConfig
from longbridge_tools.quote import QuoteSkill

# 单例模式
try:
    _config = AppConfig.load()
    _quote_skill = QuoteSkill(_config)
except Exception as e:
    print(f"Warning: Failed to load Longbridge config, quote skills will be unavailable. Error: {e}")
    _quote_skill = None

def get_stock_quote(symbols: Union[str, List[str]]) -> List[Dict]:
    """
    获取股票实时行情
    
    Args:
        symbols: 股票代码或代码列表 (e.g. "700.HK", ["AAPL.US", "BABA.US"])
        
    Returns:
        行情数据列表
    """
    if not _quote_skill:
        return []

    if isinstance(symbols, str):
        symbols = [symbols]
        
    try:
        quotes = _quote_skill.get_quote(symbols)
        return [
            {
                "symbol": q.symbol,
                "last_done": str(q.last_done),
                "open": str(q.open),
                "high": str(q.high),
                "low": str(q.low),
                "volume": q.volume,
                "turnover": str(q.turnover),
                "timestamp": q.timestamp,
                "trade_status": str(q.trade_status)
            }
            for q in quotes
        ]
    except Exception as e:
        print(f"Failed to get quote: {e}")
        return []

def get_watchlist() -> List[Dict]:
    """
    获取自选股列表 (从 Longbridge 账户同步)
    
    Returns:
        自选股列表 [{"symbol": "700.HK", "market": "HK", "name": "腾讯控股"}]
    """
    # 暂时模拟，因为 QuoteSkill.get_watchlist 似乎未实现或需要 HTTP 接口
    # 实际应调用 SDK 的 HTTP 接口获取分组
    # 这里我们假设 QuoteSkill 已经有了这个能力，或者我们扩展它
    # 根据 longport 文档，获取自选股通常需要 HTTP API，而不是 QuoteContext
    
    # 扩展 QuoteSkill 以支持 HTTP API (如果 SDK 支持)
    # 暂时返回空列表或模拟数据，等待进一步集成 HTTP API
    if not _quote_skill:
        return []

    try:
        # 假设 _quote_skill 有 get_watchlist 方法
        # 如果没有，我们需要在 QuoteSkill 中实现
        return _quote_skill.get_watchlist()
    except Exception as e:
        print(f"Failed to get watchlist: {e}")
        return []

def get_market_trades(symbol: str, count: int = 10) -> List[Dict]:
    """
    获取逐笔成交
    """
    if not _quote_skill:
        return []

    try:
        trades = _quote_skill.get_trades(symbol, count)
        return [
            {
                "price": str(t.price),
                "volume": t.volume,
                "timestamp": t.timestamp,
                "type": str(t.type),
                "direction": str(t.direction)
            }
            for t in trades
        ]
    except Exception as e:
        print(f"Failed to get trades: {e}")
        return []
