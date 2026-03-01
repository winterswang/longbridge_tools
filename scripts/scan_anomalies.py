import time
import json
from pathlib import Path
from typing import List, Dict, Any
from longbridge_tools.quote import QuoteSkill
from longbridge_tools.config import AppConfig

def determine_market(symbol: str) -> str:
    if symbol.endswith(".HK"):
        return "HK"
    elif symbol.endswith(".US"):
        return "US"
    else:
        return "CN"

def scan_anomalies():
    """
    Scan watchlist for price and trend anomalies.
    """
    print("=== Starting Anomaly Scan ===")
    
    # 1. Initialize Skill
    config = AppConfig.load()
    quote = QuoteSkill(config)
    
    # 2. Get Watchlist
    print("Fetching Watchlist...")
    groups = quote.get_watchlist()
    symbols = set()
    for group in groups:
        for security in group.securities:
            symbols.add(security.symbol)
    
    symbols = list(symbols)
    if not symbols:
        print("No symbols found in watchlist.")
        return

    print(f"Found {len(symbols)} symbols.")
    
    # 3. Get Real-time Quotes (Snapshots)
    print("Fetching Market Snapshots...")
    # longport SDK might have limit on number of symbols per request? usually 50-100 is fine.
    # Let's chunk it just in case.
    chunk_size = 50
    quotes = []
    for i in range(0, len(symbols), chunk_size):
        chunk = symbols[i:i+chunk_size]
        try:
            quotes.extend(quote.get_quote(chunk))
        except Exception as e:
            print(f"Error fetching quotes for chunk {chunk}: {e}")
            
    anomalies = []
    
    # 4. Analyze Each Stock
    print("Analyzing Stocks...")
    for q in quotes:
        symbol = q.symbol
        last_price = float(q.last_done)
        prev_close = float(q.prev_close)
        
        reasons = []
        
        # --- Check 1: Price Anomaly (> 3%) ---
        change_pct = 0.0
        if prev_close > 0:
            change_pct = (last_price - prev_close) / prev_close
            
        if abs(change_pct) > 0.03:
            reasons.append(f"Price change {change_pct*100:.2f}% exceeds ±3%")
            
        # --- Check 2: Trend Anomaly (MA20) ---
        # Only fetch history if price check passed? 
        # Requirement says "Fetch Snapshot AND History". 
        # But for efficiency, maybe we check trend for all? Or just if significant?
        # The requirement implies scanning ALL.
        
        # To avoid rate limits, we might want to sleep slightly or be robust.
        # Let's try fetching history for every stock.
        try:
            # 52 weeks ~ 1 year
            # adjust_type="forward_adjust" is better for technical analysis
            candles = quote.get_candlesticks(symbol, "week", 52, adjust_type="forward_adjust")
            
            if len(candles) >= 20:
                # Calculate MA20 (using close prices)
                closes = [float(c.close) for c in candles[-20:]]
                ma20 = sum(closes) / len(closes)
                
                if ma20 > 0:
                    deviation = (last_price - ma20) / ma20
                    
                    if deviation > 0.20:
                        reasons.append(f"Trend Surge: Price {deviation*100:.1f}% > MA20 ({ma20:.2f})")
                    elif deviation < -0.20:
                        reasons.append(f"Trend Crash: Price {abs(deviation)*100:.1f}% < MA20 ({ma20:.2f})")
                        
        except Exception as e:
            print(f"   [Warn] Failed to fetch history for {symbol}: {e}")
            
        # --- Result ---
        if reasons:
            print(f"   [ANOMALY] {symbol}: {', '.join(reasons)}")
            
            # Construct snapshot dict for downstream consumption
            snapshot = {
                "symbol": symbol,
                "last_price": last_price,
                "prev_close": prev_close,
                "open": float(q.open),
                "high": float(q.high),
                "low": float(q.low),
                "volume": int(q.volume),
                "turnover": float(q.turnover),
                "trade_status": str(q.trade_status)
            }
            
            anomalies.append({
                "symbol": symbol,
                "market": determine_market(symbol),
                "anomaly_reasons": reasons,
                "snapshot": snapshot
            })
            
    print("\n=== Scan Completed ===")
    print(f"Total Anomalies Found: {len(anomalies)}")
    
    # Save to stock_traker/data/interim/stage1_anomalies.json
    # Assuming relative path from project root or absolute path
    # Using absolute path for safety as requested
    output_path = Path("/Users/wangguangchao/code/langchain_financial/stock_traker/data/interim/stage1_anomalies.json")
    
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(anomalies, f, indent=2, ensure_ascii=False)
        print(f"Saved anomalies data to: {output_path}")
    except Exception as e:
        print(f"Error saving output: {e}")

if __name__ == "__main__":
    scan_anomalies()
