from typing import List, Dict, Optional, Union
from decimal import Decimal
from longbridge_tools.config import AppConfig
from longbridge_tools.trade import TradeSkill

# 单例模式
try:
    _config = AppConfig.load()
    _trade_skill = TradeSkill(_config)
except Exception as e:
    print(f"Warning: Failed to load Longbridge config, trade skills will be unavailable. Error: {e}")
    _trade_skill = None

def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: int,
    price: Optional[float] = None
) -> Dict:
    """
    下单
    
    Args:
        symbol: 股票代码
        side: 买卖方向 (Buy, Sell)
        order_type: 订单类型 (Market, Limit)
        quantity: 数量
        price: 价格 (仅 Limit 订单需要)
    """
    if not _trade_skill:
        return {"error": "Trade skill unavailable"}

    try:
        order_id = _trade_skill.place_order(symbol, side, order_type, quantity, price)
        return {"order_id": order_id, "status": "submitted"}
    except Exception as e:
        print(f"Failed to place order: {e}")
        return {"error": str(e)}

def get_orders(symbol: Optional[str] = None) -> List[Dict]:
    """
    查询订单列表
    """
    if not _trade_skill:
        return []

    try:
        orders = _trade_skill.get_orders(symbol)
        return [
            {
                "order_id": o.order_id,
                "symbol": o.symbol,
                "status": str(o.status),
                "side": str(o.side),
                "type": str(o.order_type),
                "price": str(o.price),
                "quantity": o.quantity,
                "filled_quantity": o.filled_quantity
            }
            for o in orders
        ]
    except Exception as e:
        print(f"Failed to get orders: {e}")
        return []
