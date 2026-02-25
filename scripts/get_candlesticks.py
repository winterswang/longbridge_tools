import sys
import os
from pathlib import Path
from datetime import datetime

# Add src directory to sys.path to allow importing longbridge_tools without installation
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from longbridge_tools import QuoteSkill

def main():
    try:
        # Initialize QuoteSkill
        skill = QuoteSkill()
        
        # Define symbols to fetch
        # PDD (US Market), Tencent (HK Market)
        symbols = ["PDD.US", "700.HK"]
        
        print(f"Fetching historical candlesticks for: {', '.join(symbols)}")
        print("-" * 50)
        
        for symbol in symbols:
            print(f"\nFetching data for {symbol}...")
            
            # Fetch daily candlesticks, last 10 days
            # period="day", count=10, adjust_type="no_adjust" (default)
            candlesticks = skill.get_candlesticks(symbol, "day", 10)
            
            if not candlesticks:
                print(f"  No data found for {symbol}")
                continue
                
            print(f"  Found {len(candlesticks)} records (Last 10 days):")
            print(f"  {'Date':<12} | {'Open':<10} | {'High':<10} | {'Low':<10} | {'Close':<10} | {'Volume':<12}")
            print("  " + "-" * 70)
            
            for k in candlesticks:
                # Assuming candlestick object has these attributes
                # Note: timestamp might be int (unix) or datetime object depending on SDK version
                # If it's already a datetime object, format it directly
                ts = k.timestamp
                if isinstance(ts, datetime):
                    date_str = ts.strftime('%Y-%m-%d')
                else:
                    # Try converting from int/float timestamp
                    try:
                        date_str = datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d')
                    except:
                        date_str = str(ts)
                
                print(f"  {date_str:<12} | {k.open:<10} | {k.high:<10} | {k.low:<10} | {k.close:<10} | {k.volume:<12}")
                
        print("-" * 50)

    except Exception as e:
        print(f"Error fetching candlesticks: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
