"""
Sky map processing and manipulation utilities.

This module provides the SkyMap class and related functions for working
with astronomical sky maps, including coordinate transformations, 
statistics, and visualization.
"""

import numpy as np
from typing import Optional, Union, Tuple, Dict, Any
import warnings


class SkyMapError(Exception):
    """Exception raised for sky map related errors."""
    pass


class SkyMap:
    """
    A class to represent and manipulate astronomical sky maps.
    
    This class provides a convenient interface for working with sky maps,
    including pixel-based operations, coordinate transformations, and
    statistical analysis.
    
    Parameters
    ----------
    data : np.ndarray
        Sky map data array
    nside : int, optional
        HEALPix nside parameter for spherical maps
    coordinate_system : str, optional
        Coordinate system ('galactic', 'equatorial', 'ecliptic')
    units : str, optional
        Physical units of the map values
    metadata : dict, optional
        Additional metadata about the map
    """
    
    def __init__(
        self,
        data: np.ndarray,
        nside: Optional[int] = None,
        coordinate_system: str = "galactic", 
        units: str = "unknown",
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.data = np.asarray(data)
        self.nside = nside
        self.coordinate_system = coordinate_system
        self.units = units
        self.metadata = metadata or {}
        
        # Validate inputs
        if self.data.ndim not in [1, 2]:
            raise SkyMapError("Sky map data must be 1D or 2D array")
            
        if nside is not None and nside <= 0:
            raise SkyMapError("nside must be positive")
    
    @property
    def npix(self) -> int:
        """Number of pixels in the map."""
        return self.data.size
    
    @property
    def shape(self) -> Tuple[int, ...]:
        """Shape of the map data."""
        return self.data.shape
    
    @property 
    def resolution(self) -> Optional[float]:
        """Angular resolution in arcminutes (for HEALPix maps)."""
        if self.nside is None:
            return None
        # Approximate resolution for HEALPix maps
        return np.sqrt(3.0 / np.pi) * 180.0 * 60.0 / self.nside
    
    def copy(self) -> "SkyMap":
        """Create a copy of the sky map."""
        return SkyMap(
            data=self.data.copy(),
            nside=self.nside,
            coordinate_system=self.coordinate_system,
            units=self.units,
            metadata=self.metadata.copy()
        )
    
    def get_stats(self) -> Dict[str, float]:
        """
        Calculate basic statistics of the map.
        
        Returns
        -------
        Dict[str, float]
            Dictionary with mean, std, min, max, and other statistics
        """
        valid_data = self.data[np.isfinite(self.data)]
        
        if len(valid_data) == 0:
            return {
                "mean": np.nan,
                "std": np.nan,
                "min": np.nan,
                "max": np.nan,
                "median": np.nan,
                "valid_pixels": 0,
                "total_pixels": self.npix
            }
        
        return {
            "mean": float(np.mean(valid_data)),
            "std": float(np.std(valid_data)),
            "min": float(np.min(valid_data)),
            "max": float(np.max(valid_data)),
            "median": float(np.median(valid_data)),
            "valid_pixels": len(valid_data),
            "total_pixels": self.npix
        }
    
    def mask_pixels(self, mask: np.ndarray, fill_value: float = np.nan) -> None:
        """
        Apply a mask to the sky map.
        
        Parameters
        ----------
        mask : np.ndarray
            Boolean mask array (True = keep, False = mask)
        fill_value : float, optional
            Value to use for masked pixels. Default is np.nan
        """
        if mask.shape != self.data.shape:
            raise SkyMapError("Mask shape must match data shape")
        
        self.data[~mask] = fill_value
    
    def smooth(self, fwhm: float) -> "SkyMap":
        """
        Smooth the sky map with a Gaussian kernel.
        
        Parameters
        ----------
        fwhm : float
            Full width at half maximum of the smoothing kernel in arcminutes
            
        Returns
        -------
        SkyMap
            Smoothed sky map
            
        Notes
        -----
        This is a placeholder implementation. Real smoothing would require
        proper spherical harmonic transforms.
        """
        warnings.warn("Smoothing is not yet fully implemented", UserWarning)
        
        # Placeholder - return a copy for now
        smoothed = self.copy()
        # In a real implementation, this would use healpy.smoothing or similar
        return smoothed
    
    def downgrade(self, factor: int) -> "SkyMap":
        """
        Downgrade the resolution of the map.
        
        Parameters
        ----------
        factor : int
            Downgrading factor
            
        Returns
        -------
        SkyMap
            Downgraded sky map
        """
        warnings.warn("Downgrading is not yet fully implemented", UserWarning)
        
        # Placeholder implementation
        if self.data.ndim == 1:
            # For 1D data, simple decimation
            downgraded_data = self.data[::factor]
        else:
            # For 2D data, block averaging
            h, w = self.data.shape
            new_h, new_w = h // factor, w // factor
            downgraded_data = self.data[:new_h*factor, :new_w*factor].reshape(
                new_h, factor, new_w, factor
            ).mean(axis=(1, 3))
        
        new_nside = self.nside // factor if self.nside is not None else None
        
        return SkyMap(
            data=downgraded_data,
            nside=new_nside,
            coordinate_system=self.coordinate_system,
            units=self.units,
            metadata=self.metadata.copy()
        )
    
    def __repr__(self) -> str:
        """String representation of the SkyMap."""
        stats = self.get_stats()
        return (
            f"SkyMap(shape={self.shape}, nside={self.nside}, "
            f"coordinate_system='{self.coordinate_system}', "
            f"units='{self.units}', mean={stats['mean']:.3e}, "
            f"std={stats['std']:.3e})"
        )


def load_skymap(filename: str, **kwargs: Any) -> SkyMap:
    """
    Load a sky map from file.
    
    Parameters
    ----------
    filename : str
        Path to the file to load
    **kwargs : Any
        Additional arguments passed to the appropriate loader
        
    Returns
    -------
    SkyMap
        Loaded sky map object
    """
    # Import here to avoid circular imports
    from .io import load_fits, load_healpix
    
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.fits') or filename_lower.endswith('.fit'):
        data, metadata = load_fits(filename, **kwargs)
        nside = metadata.get('nside')
        coord_sys = metadata.get('coordinate_system', 'galactic')
        units = metadata.get('units', 'unknown')
        
        return SkyMap(
            data=data,
            nside=nside,
            coordinate_system=coord_sys,
            units=units,
            metadata=metadata
        )
    else:
        raise SkyMapError(f"Unsupported file format: {filename}")


def save_skymap(skymap: SkyMap, filename: str, **kwargs: Any) -> None:
    """
    Save a sky map to file.
    
    Parameters
    ----------
    skymap : SkyMap
        Sky map to save
    filename : str
        Output filename
    **kwargs : Any
        Additional arguments passed to the appropriate writer
    """
    # Import here to avoid circular imports
    from .io import save_fits
    
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.fits') or filename_lower.endswith('.fit'):
        # Prepare metadata
        metadata = skymap.metadata.copy()
        if skymap.nside is not None:
            metadata['nside'] = skymap.nside
        metadata['coordinate_system'] = skymap.coordinate_system
        metadata['units'] = skymap.units
        
        save_fits(skymap.data, filename, metadata=metadata, **kwargs)
    else:
        raise SkyMapError(f"Unsupported file format: {filename}")


def create_random_skymap(
    nside: int = 64,
    seed: Optional[int] = None,
    coordinate_system: str = "galactic"
) -> SkyMap:
    """
    Create a random sky map for testing purposes.
    
    Parameters
    ----------
    nside : int, optional
        HEALPix nside parameter. Default is 64
    seed : int, optional
        Random seed for reproducibility
    coordinate_system : str, optional
        Coordinate system. Default is 'galactic'
        
    Returns
    -------
    SkyMap
        Random sky map
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Create HEALPix map
    npix = 12 * nside**2
    data = np.random.normal(0, 1, npix)
    
    return SkyMap(
        data=data,
        nside=nside,
        coordinate_system=coordinate_system,
        units="arbitrary",
        metadata={"created": "random", "seed": seed}
    )