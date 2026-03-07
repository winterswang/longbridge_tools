from typing import List, Dict, Optional
from longbridge_tools.config import AppConfig
from longbridge_tools.asset import AssetSkill

# 单例模式
try:
    _config = AppConfig.load()
    _asset_skill = AssetSkill(_config)
except Exception as e:
    print(f"Warning: Failed to load Longbridge config, asset skills will be unavailable. Error: {e}")
    _asset_skill = None

def get_account_asset() -> Dict:
    """
    获取账户资产概览
    """
    if not _asset_skill:
        return {}

    try:
        asset = _asset_skill.get_asset()
        return {
            "total_assets": str(asset.total_assets),
            "available_cash": str(asset.available_cash),
            "frozen_cash": str(asset.frozen_cash),
            "settled_cash": str(asset.settled_cash),
            "currency": asset.currency,
        }
    except Exception as e:
        print(f"Failed to get asset: {e}")
        return {}

def get_positions() -> List[Dict]:
    """
    获取持仓列表
    """
    if not _asset_skill:
        return []

    try:
        positions = _asset_skill.get_positions()
        return [
            {
                "symbol": p.symbol,
                "quantity": p.quantity,
                "cost_price": str(p.cost_price),
                "current_price": str(p.current_price),
                "market_value": str(p.market_value),
                "unrealized_pnl": str(p.unrealized_pnl),
                "unrealized_pnl_rate": str(p.unrealized_pnl_rate)
            }
            for p in positions
        ]
    except Exception as e:
        print(f"Failed to get positions: {e}")
        return []
