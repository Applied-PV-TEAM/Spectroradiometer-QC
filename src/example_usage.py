"""
Example usage of the data_loader module.

This script demonstrates how to use the data loading functions.
"""

from data_loader import load_parquet_data, get_available_data

def main():
    """Demonstrate data loading functionality."""
    
    print("=== Spectroradiometer Data Loader Example ===\n")
    
    # 1. Check what data is available
    print("1. Checking available data...")
    available_data = get_available_data()
    
    for station, months in available_data.items():
        print(f"   {station}: {len(months)} months available")
        if months:
            print(f"     Range: {months[0]} to {months[-1]}")
    
    print()
    
    # 2. Load specific data if DTU data is available
    if available_data.get('DTU'):
        print("2. Loading DTU data for June 2024...")
        try:
            df = load_parquet_data('DTU', 6, 2024)
            print(f"   ✓ Loaded {df.shape[0]:,} rows and {df.shape[1]:,} columns")
            print(f"   ✓ Columns include: {', '.join(df.columns[:5])}...")
            
            # Show some basic info about the data
            if 'Global_Horizontal_Pyr' in df.columns:
                print(f"   ✓ Global Horizontal data range: {df['Global_Horizontal_Pyr'].min():.1f} to {df['Global_Horizontal_Pyr'].max():.1f}")
                
        except Exception as e:
            print(f"   ✗ Error loading data: {e}")
    
    print()
    
    # 3. Demonstrate different ways to specify months
    print("3. Different ways to specify months:")
    examples = [
        ("DTU", 6, 2024, "Using month number"),
        ("DTU", "June", 2024, "Using month name"),
        ("DTU", "Jun", 2024, "Using month abbreviation"),
    ]
    
    for station, month, year, description in examples:
        try:
            df = load_parquet_data(station, month, year)
            print(f"   ✓ {description}: {df.shape[0]:,} rows loaded")
        except Exception as e:
            print(f"   ✗ {description}: {e}")

if __name__ == "__main__":
    main()
