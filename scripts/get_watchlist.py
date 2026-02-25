from longbridge_tools import QuoteSkill

def main():
    try:
        # Initialize QuoteSkill (automatically loads config from env or file)
        skill = QuoteSkill()
        print("Fetching watchlist...")
        
        # Get all watchlist groups
        groups = skill.get_watchlist()
        
        if not groups:
            print("No watchlist groups found.")
            return

        print(f"Found {len(groups)} watchlist groups:")
        print("-" * 40)
        
        for group in groups:
            print(f"\nGroup Name: {group.name} (ID: {group.id})")
            
            # Check if securities list is available and not empty
            # Note: The SDK might return securities as a list of objects or similar structure
            if not hasattr(group, 'securities') or not group.securities:
                print("  (No securities in this group)")
                continue
                
            print(f"  Securities ({len(group.securities)}):")
            for sec in group.securities:
                # Access symbol and market from security object
                # Assuming security object has symbol and market attributes
                symbol = getattr(sec, 'symbol', 'Unknown')
                market = getattr(sec, 'market', 'Unknown')
                name = getattr(sec, 'name', '') # Name might be optional
                
                info = f"{symbol}.{market}"
                if name:
                    info += f" ({name})"
                print(f"  - {info}")
                
        print("-" * 40)
                
    except Exception as e:
        print(f"Error fetching watchlist: {e}")
        # Print more detail if available
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
