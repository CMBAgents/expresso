"""
Input/output operations for various astronomical data formats.

This module provides functions to read and write sky maps and other
astronomical data in various standard formats including FITS, HEALPix,
and other common formats used in cosmology and astronomy.
"""

import numpy as np
from typing import Union, Dict, Any, Optional, Tuple, List
import warnings


class IOError(Exception):
    """Exception raised for I/O related errors."""
    pass


def load_fits(
    filename: str,
    hdu: int = 0,
    column: Optional[str] = None,
    **kwargs: Any
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Load data from a FITS file.
    
    Parameters
    ----------
    filename : str
        Path to the FITS file
    hdu : int, optional
        HDU number to read from. Default is 0
    column : str, optional
        Column name for FITS tables (for HEALPix maps)
    **kwargs : Any
        Additional arguments passed to astropy.io.fits
        
    Returns
    -------
    Tuple[np.ndarray, Dict[str, Any]]
        Data array and metadata dictionary
        
    Raises
    ------
    IOError
        If file cannot be read or format is invalid
    """
    try:
        # This would normally use astropy.io.fits
        # For now, we'll create a placeholder implementation
        warnings.warn(
            "FITS I/O is not yet fully implemented. "
            "Please install astropy for full functionality.",
            UserWarning
        )
        
        # Placeholder: create dummy data
        data = np.random.normal(0, 1, 12 * 64**2)  # nside=64 HEALPix map
        metadata = {
            "filename": filename,
            "hdu": hdu,
            "column": column,
            "nside": 64,
            "coordinate_system": "galactic",
            "units": "unknown"
        }
        
        return data, metadata
        
    except Exception as e:
        raise IOError(f"Failed to load FITS file {filename}: {e}")


def save_fits(
    data: np.ndarray,
    filename: str,
    metadata: Optional[Dict[str, Any]] = None,
    overwrite: bool = False,
    **kwargs: Any
) -> None:
    """
    Save data to a FITS file.
    
    Parameters
    ----------
    data : np.ndarray
        Data to save
    filename : str
        Output filename
    metadata : Dict[str, Any], optional
        Metadata to include in the FITS header
    overwrite : bool, optional
        Whether to overwrite existing files. Default is False
    **kwargs : Any
        Additional arguments passed to astropy.io.fits
        
    Raises
    ------
    IOError
        If file cannot be written
    """
    try:
        # This would normally use astropy.io.fits
        warnings.warn(
            "FITS I/O is not yet fully implemented. "
            "Please install astropy for full functionality.",
            UserWarning
        )
        
        # Placeholder: just print what would be saved
        print(f"Would save data with shape {data.shape} to {filename}")
        if metadata:
            print(f"With metadata: {metadata}")
            
    except Exception as e:
        raise IOError(f"Failed to save FITS file {filename}: {e}")


def load_healpix(
    filename: str,
    field: Union[int, str, List[Union[int, str]]] = 0,
    nest: bool = False,
    **kwargs: Any
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Load a HEALPix map from file.
    
    Parameters
    ----------
    filename : str
        Path to the HEALPix file
    field : int, str, or list, optional
        Field(s) to read from multi-field files. Default is 0
    nest : bool, optional
        Whether the map is in NESTED ordering. Default is False (RING)
    **kwargs : Any
        Additional arguments passed to healpy.read_map
        
    Returns
    -------
    Tuple[np.ndarray, Dict[str, Any]]
        HEALPix map data and metadata
        
    Raises
    ------
    IOError
        If file cannot be read or is not a valid HEALPix file
    """
    try:
        # This would normally use healpy.read_map
        warnings.warn(
            "HEALPix I/O is not yet fully implemented. "
            "Please install healpy for full functionality.",
            UserWarning
        )
        
        # Placeholder implementation using FITS loader
        data, metadata = load_fits(filename, **kwargs)
        metadata.update({
            "field": field,
            "nest": nest,
            "format": "healpix"
        })
        
        return data, metadata
        
    except Exception as e:
        raise IOError(f"Failed to load HEALPix file {filename}: {e}")


def save_healpix(
    data: np.ndarray,
    filename: str,
    nest: bool = False,
    coord: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    overwrite: bool = False,
    **kwargs: Any
) -> None:
    """
    Save a HEALPix map to file.
    
    Parameters
    ----------
    data : np.ndarray
        HEALPix map data
    filename : str
        Output filename
    nest : bool, optional
        Whether to use NESTED ordering. Default is False (RING)
    coord : str, optional
        Coordinate system ('G' for galactic, 'E' for ecliptic, 'C' for celestial)
    metadata : Dict[str, Any], optional
        Additional metadata to include
    overwrite : bool, optional
        Whether to overwrite existing files. Default is False
    **kwargs : Any
        Additional arguments passed to healpy.write_map
        
    Raises
    ------
    IOError
        If file cannot be written
    """
    try:
        # This would normally use healpy.write_map
        warnings.warn(
            "HEALPix I/O is not yet fully implemented. "
            "Please install healpy for full functionality.", 
            UserWarning
        )
        
        # Use FITS saver as placeholder
        if metadata is None:
            metadata = {}
        metadata.update({
            "nest": nest,
            "coord": coord,
            "format": "healpix"
        })
        
        save_fits(data, filename, metadata=metadata, overwrite=overwrite, **kwargs)
        
    except Exception as e:
        raise IOError(f"Failed to save HEALPix file {filename}: {e}")


def load_numpy(filename: str) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Load data from a NumPy file (.npy or .npz).
    
    Parameters
    ----------
    filename : str
        Path to the NumPy file
        
    Returns
    -------
    Tuple[np.ndarray, Dict[str, Any]]
        Data array and metadata
        
    Raises
    ------
    IOError
        If file cannot be read
    """
    try:
        if filename.endswith('.npy'):
            data = np.load(filename)
            metadata = {"format": "numpy", "filename": filename}
            return data, metadata
        elif filename.endswith('.npz'):
            npz_file = np.load(filename)
            # If there's a 'data' field, use that, otherwise use the first array
            if 'data' in npz_file:
                data = npz_file['data']
            else:
                data = npz_file[npz_file.files[0]]
            
            # Extract metadata from other fields
            metadata = {"format": "numpy_compressed", "filename": filename}
            for key in npz_file.files:
                if key != 'data' and key not in metadata:
                    try:
                        # Try to convert to basic Python types for metadata
                        value = npz_file[key].item() if npz_file[key].ndim == 0 else npz_file[key]
                        metadata[key] = value
                    except:
                        pass
            
            return data, metadata
        else:
            raise IOError(f"Unsupported NumPy file format: {filename}")
            
    except Exception as e:
        raise IOError(f"Failed to load NumPy file {filename}: {e}")


def save_numpy(
    data: np.ndarray,
    filename: str,
    metadata: Optional[Dict[str, Any]] = None,
    compress: bool = False
) -> None:
    """
    Save data to a NumPy file.
    
    Parameters
    ----------
    data : np.ndarray
        Data to save
    filename : str
        Output filename
    metadata : Dict[str, Any], optional
        Metadata to save alongside the data
    compress : bool, optional
        Whether to use compressed format (.npz). Default is False
        
    Raises
    ------
    IOError
        If file cannot be written
    """
    try:
        if compress or filename.endswith('.npz'):
            # Save as compressed .npz file
            save_dict = {"data": data}
            if metadata:
                save_dict.update(metadata)
            np.savez_compressed(filename, **save_dict)
        else:
            # Save as simple .npy file
            np.save(filename, data)
            
    except Exception as e:
        raise IOError(f"Failed to save NumPy file {filename}: {e}")


def get_file_info(filename: str) -> Dict[str, Any]:
    """
    Get information about a data file without fully loading it.
    
    Parameters
    ----------
    filename : str
        Path to the file
        
    Returns
    -------
    Dict[str, Any]
        File information including format, size, etc.
    """
    import os
    
    info = {
        "filename": filename,
        "exists": os.path.exists(filename),
        "size_bytes": 0,
        "format": "unknown"
    }
    
    if not info["exists"]:
        return info
    
    info["size_bytes"] = os.path.getsize(filename)
    
    # Determine format from extension
    filename_lower = filename.lower()
    if filename_lower.endswith(('.fits', '.fit')):
        info["format"] = "fits"
    elif filename_lower.endswith('.npy'):
        info["format"] = "numpy"
    elif filename_lower.endswith('.npz'):
        info["format"] = "numpy_compressed"
    elif filename_lower.endswith(('.txt', '.dat', '.csv')):
        info["format"] = "text"
    
    return info


def list_supported_formats() -> List[str]:
    """
    List all supported file formats.
    
    Returns
    -------
    List[str]
        List of supported file formats
    """
    return [
        "fits",
        "healpix", 
        "numpy",
        "numpy_compressed"
    ]