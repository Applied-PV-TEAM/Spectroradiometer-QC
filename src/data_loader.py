"""
Data loading and saving utilities for Spectroradiometer QC project.

This module provides functions to load and save spectroradiometer data
from various stations (DTU, WUT) organized by month.
"""

import os
import pandas as pd
from pathlib import Path
from typing import Optional, Union
from datetime import datetime
import calendar


def load_parquet_data(station: str, month: Union[int, str], year: Optional[int] = None) -> pd.DataFrame:
    """
    Load parquet data for a specific station and month.
    
    Args:
        station (str): Station code ('DTU' or 'WUT')
        month (Union[int, str]): Month number (1-12) or month name
        year (Optional[int]): Year (defaults to 2024 if not specified)
    
    Returns:
        pd.DataFrame: Loaded parquet data
        
    Raises:
        ValueError: If station or month is invalid
        FileNotFoundError: If the parquet file doesn't exist
        
    Examples:
        >>> data = load_parquet_data('DTU', 6, 2024)  # June 2024
        >>> data = load_parquet_data('DTU', 'June', 2024)
        >>> data = load_parquet_data('WUT', 12)  # December 2024 (default year)
    """
    # Validate and normalize inputs
    station = station.upper()
    if station not in ['DTU', 'WUT']:
        raise ValueError(f"Invalid station '{station}'. Must be 'DTU' or 'WUT'")
    
    # Handle year default
    if year is None:
        year = 2024
    
    # Convert month name to number if needed
    if isinstance(month, str):
        try:
            month = list(calendar.month_name).index(month.capitalize())
        except ValueError:
            try:
                month = list(calendar.month_abbr).index(month.capitalize()[:3])
            except ValueError:
                raise ValueError(f"Invalid month name '{month}'")
    
    # Validate month number
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month '{month}'. Must be between 1 and 12")
    
    # Get the last day of the month
    last_day = calendar.monthrange(year, month)[1]
    
    # Construct the filename based on the observed pattern
    filename = f"{station}_{year}-{month:02d}-01_to_{year}-{month:02d}-{last_day:02d}.parquet"
    
    # Determine the data folder path
    current_dir = Path(__file__).parent.parent  # Go up from src/ to project root
    
    # Check different possible locations for the data
    possible_paths = [
        current_dir / "data" / f"{station.lower()}_combined" / filename,  # DTU pattern
        current_dir / "data" / f"{station.lower()}_data" / filename,      # Alternative pattern
        current_dir / "data" / filename,                                  # Direct in data folder
    ]
    
    # Try to find the file
    file_path = None
    for path in possible_paths:
        if path.exists():
            file_path = path
            break
    
    if file_path is None:
        # Create a helpful error message showing what was searched
        searched_paths = [str(p) for p in possible_paths]
        raise FileNotFoundError(
            f"Could not find parquet file for {station} station, "
            f"{calendar.month_name[month]} {year}.\n"
            f"Searched in:\n" + "\n".join(f"  - {p}" for p in searched_paths)
        )
    
    try:
        # Load the parquet file
        df = pd.read_parquet(file_path)
        print(f"Successfully loaded {len(df)} records from {file_path.name}")
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading parquet file {file_path}: {str(e)}")


def get_available_data(station: Optional[str] = None) -> dict:
    """
    Get information about available parquet files.
    
    Args:
        station (Optional[str]): Filter by station ('DTU' or 'WUT'). 
                               If None, returns data for all stations.
    
    Returns:
        dict: Dictionary with station names as keys and lists of available 
              (year, month) tuples as values
    """
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / "data"
    
    available_data = {}
    
    # Define stations to check
    stations_to_check = [station.upper()] if station else ['DTU', 'WUT']
    
    for station_name in stations_to_check:
        available_data[station_name] = []
        
        # Check different possible subdirectories
        subdirs = [
            f"{station_name.lower()}_combined",
            f"{station_name.lower()}_data",
            ""  # Direct in data folder
        ]
        
        for subdir in subdirs:
            search_dir = data_dir / subdir if subdir else data_dir
            if not search_dir.exists():
                continue
                
            # Look for parquet files matching the pattern
            pattern = f"{station_name}_*.parquet"
            for file_path in search_dir.glob(pattern):
                try:
                    # Extract year and month from filename
                    # Expected format: STATION_YYYY-MM-DD_to_YYYY-MM-DD.parquet
                    parts = file_path.stem.split('_')
                    if len(parts) >= 2:
                        date_part = parts[1]  # YYYY-MM-DD
                        year, month, _ = date_part.split('-')
                        available_data[station_name].append((int(year), int(month)))
                except (ValueError, IndexError):
                    continue
        
        # Remove duplicates and sort
        available_data[station_name] = sorted(list(set(available_data[station_name])))
    
    return available_data


# Future functions for saving data can be added here
def save_parquet_data(df: pd.DataFrame, station: str, month: int, year: int, 
                     subfolder: str = "processed") -> Path:
    """
    Save DataFrame as parquet file (placeholder for future implementation).
    
    Args:
        df (pd.DataFrame): Data to save
        station (str): Station code
        month (int): Month number
        year (int): Year
        subfolder (str): Subfolder within data directory
        
    Returns:
        Path: Path to saved file
    """
    # This is a placeholder - implement when needed
    raise NotImplementedError("save_parquet_data not yet implemented")
