"""
Expresso: Tools to compress and express information from maps of the sky.

This package provides utilities for processing, compressing, and analyzing
astronomical sky maps, particularly focused on cosmic microwave background
(CMB) data and other cosmological observations.

Main modules:
- compression: Data compression algorithms for sky maps
- skymap: Sky map processing and manipulation utilities  
- io: Input/output operations for various astronomical data formats
- utils: General utility functions and helpers
- config: Configuration management
"""

__version__ = "0.1.0"
__author__ = "CMBAgents"
__email__ = "contact@cmbagents.org"

# Import main functionality for convenient access
from .compression import compress_skymap, decompress_skymap, get_compression_info
from .skymap import SkyMap, load_skymap, save_skymap, create_random_skymap
from .io import load_fits, save_fits, load_healpix, save_healpix
from .utils import get_resolution, angular_distance, pixel_area
from . import config

__all__ = [
    # Version info
    "__version__", 
    "__author__", 
    "__email__",
    
    # Compression functionality
    "compress_skymap",
    "decompress_skymap",
    "get_compression_info",
    
    # Sky map operations
    "SkyMap",
    "load_skymap", 
    "save_skymap",
    "create_random_skymap",
    
    # I/O operations
    "load_fits",
    "save_fits", 
    "load_healpix",
    "save_healpix",
    
    # Utilities
    "get_resolution",
    "angular_distance", 
    "pixel_area",
    
    # Configuration
    "config",
]