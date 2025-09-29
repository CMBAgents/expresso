# Expresso

**Tools to compress and express information from maps of the sky**

Expresso is a Python package designed for processing, compressing, and analyzing astronomical sky maps, with a particular focus on cosmic microwave background (CMB) data and other cosmological observations.

## Features

- **Sky Map Processing**: Load, manipulate, and analyze astronomical sky maps
- **Data Compression**: Advanced compression algorithms optimized for astronomical data
- **Multiple Formats**: Support for FITS, HEALPix, and other standard astronomical formats
- **Coordinate Systems**: Handle different coordinate systems (galactic, equatorial, ecliptic)
- **Command Line Interface**: Easy-to-use CLI tools for common operations
- **Extensible**: Modular design for easy extension and customization

## Installation

### From PyPI (when available)
```bash
pip install expresso
```

### From Source
```bash
git clone https://github.com/CMBAgents/expresso.git
cd expresso
pip install -e .
```

### Dependencies

Core dependencies:
- `numpy >= 1.20.0`
- `scipy >= 1.7.0`
- `astropy >= 5.0.0` (for FITS I/O)
- `healpy >= 1.15.0` (for HEALPix support)

Development dependencies:
- `pytest >= 6.0.0` (for testing)
- `black >= 22.0.0` (for code formatting)
- `mypy >= 0.950` (for type checking)

## Quick Start

### Basic Usage

```python
import expresso

# Create a random sky map for testing
skymap = expresso.create_random_skymap(nside=64, seed=42)

# Get basic statistics
stats = skymap.get_stats()
print(f"Mean: {stats['mean']:.3e}, Std: {stats['std']:.3e}")

# Compress the sky map
compressed_data = expresso.compress_skymap(
    skymap.data, 
    method="wavelet", 
    compression_ratio=0.1
)

# Get compression info
info = expresso.get_compression_info(compressed_data)
print(f"Space saved: {info['space_saved_percent']:.1f}%")

# Decompress
decompressed_data = expresso.decompress_skymap(compressed_data)
```

### Loading and Saving Sky Maps

```python
# Load a sky map from FITS file
skymap = expresso.load_skymap("data/skymap.fits")

# Process the sky map
smoothed = skymap.smooth(fwhm=5.0)  # 5 arcmin FWHM
downgraded = skymap.downgrade(factor=2)

# Save processed sky map
expresso.save_skymap(smoothed, "output/smoothed_map.fits")
```

### Command Line Interface

```bash
# Compress a sky map
expresso compress input.fits output.compressed --method wavelet --ratio 0.1

# Get information about a compressed file
expresso info output.compressed

# Generate a random sky map for testing
expresso generate test_map.fits --nside 128 --seed 42

# Get statistics about a sky map
expresso stats input.fits
```

## Package Structure

```
expresso/
├── __init__.py          # Main package interface
├── compression.py       # Data compression algorithms
├── skymap.py           # Sky map processing and manipulation
├── io.py               # Input/output operations
├── utils.py            # Utility functions and helpers
├── config.py           # Configuration management
├── cli.py              # Command-line interface
├── tests/              # Test suite
│   └── test_*.py
└── examples/           # Usage examples
    └── basic_usage.py
```

## Modules

### `expresso.compression`
Advanced compression algorithms for astronomical data:
- Wavelet-based compression
- Principal Component Analysis (PCA)
- Singular Value Decomposition (SVD)
- Configurable compression ratios and quality settings

### `expresso.skymap`
Sky map processing and manipulation:
- `SkyMap` class for representing astronomical sky maps
- Coordinate system transformations
- Statistical analysis and masking
- Smoothing and resolution changes

### `expresso.io`
Input/output operations for various formats:
- FITS file support via astropy
- HEALPix format support via healpy
- NumPy array formats
- Metadata preservation

### `expresso.utils`
Utility functions for astronomical calculations:
- Angular distance calculations
- Coordinate transformations
- Unit conversions
- Beam functions and physical constants

### `expresso.config`
Configuration management:
- Default settings and parameter validation
- User configuration files
- Runtime configuration updates

## Examples

See the `examples/` directory for detailed usage examples:

- `basic_usage.py`: Comprehensive example showing core functionality
- More examples coming soon!

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=expresso
```

### Code Style

This project uses `black` for code formatting and `mypy` for type checking:

```bash
# Format code
black expresso/

# Type checking
mypy expresso/
```

## Contributing

Contributions are welcome! Please see the contributing guidelines for details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for the cosmic microwave background (CMB) and cosmology community
- Designed to work with standard astronomical data formats and tools
- Inspired by the need for efficient storage and transmission of large sky maps

## Support

- **Documentation**: [GitHub README](https://github.com/CMBAgents/expresso#readme)
- **Issues**: [GitHub Issues](https://github.com/CMBAgents/expresso/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CMBAgents/expresso/discussions)
