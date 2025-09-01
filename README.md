# Spectroradiometer Quality Control

A Python library for quality control and analysis of spectroradiometer data from various stations (DTU, WUT).

## Features

- 📊 **Data Loading**: Efficient loading of parquet files organized by station and month
- 🔍 **Quality Control**: Comprehensive QC checks for spectroradiometer data
- 🌤️ **SMARTS Integration**: Atmospheric modeling capabilities
- 📈 **Visualization**: Tools for visualizing QC results and data

## Installation

### Install from local directory (development)

```bash
# Clone or navigate to the project directory
cd /path/to/spectroradiometer-qc

# Install in development mode
pip install -e .

# Or install with optional dependencies
pip install -e .[dev,viz,jupyter]
```

### Install all dependencies

```bash
pip install -e .[all]
```

## Quick Start

```python
import spectroradiometer_qc as sqc

# Load DTU data for June 2024
data = sqc.load_parquet_data('DTU', 6, 2024)

# Initialize quality control
qc = sqc.SpectralQC(data, column_mapping={})

# Run QC checks
qc.greater_than_zero_check()
qc.not_a_number_check()

# Check available data
available = sqc.get_available_data('DTU')
print(f"Available DTU data: {len(available['DTU'])} months")
```

## Project Structure

```
spectroradiometer-qc/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── data_loader.py           # Data loading utilities
│   ├── quality_control.py       # QC checks and SpectralQC class
│   ├── SMARTS.py               # SMARTS atmospheric modeling
│   ├── python_smarts.py        # SMARTS Python interface
│   └── viualisation.py         # Visualization tools
├── data/                        # Data files
│   └── dtu_combined/           # DTU parquet files
├── tests/                       # Test files (coming soon)
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## Development

### Dependencies

Core dependencies:
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `pyarrow` - Efficient parquet file handling

Optional dependencies:
- `matplotlib`, `seaborn`, `plotly` - Visualization
- `jupyter` - Notebook support
- `pytest` - Testing framework

### Development Setup

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/
```

## Data Format

The library expects parquet files organized as:
```
data/{station}_combined/{STATION}_YYYY-MM-DD_to_YYYY-MM-DD.parquet
```

Example: `data/dtu_combined/DTU_2024-06-01_to_2024-06-30.parquet`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **Repository**: https://github.com/yourusername/spectroradiometer-qc
