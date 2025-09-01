"""
Spectroradiometer Quality Control (spectroradiometer-qc)

A Python library for quality control and analysis of spectroradiometer data,
particularly for DTU and WUT stations.

Main modules:
- data_loader: Functions for loading and saving parquet data files
- quality_control: SpectralQC class for performing quality control checks
- SMARTS: SMARTS model integration for atmospheric modeling
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import main classes and functions for easy access
from .data_loader import load_parquet_data, get_available_data, save_parquet_data
from .quality_control import SpectralQC
from .viualisation import SpectralQCVisualization

# Define what gets imported with "from spectroradiometer_qc import *"
__all__ = [
    "load_parquet_data",
    "get_available_data", 
    "save_parquet_data",
    "SpectralQC",
    "SpectralQCVisualization",
    "__version__"
]
