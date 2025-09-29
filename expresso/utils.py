"""
General utility functions and helpers for astronomical data processing.

This module provides various utility functions for coordinate transformations,
angular calculations, unit conversions, and other common operations needed
when working with astronomical sky maps and cosmological data.
"""

import numpy as np
from typing import Union, Tuple, Optional, Any
import warnings


def get_resolution(nside: int) -> float:
    """
    Calculate the angular resolution of a HEALPix map.
    
    Parameters
    ----------
    nside : int
        HEALPix nside parameter
        
    Returns
    -------
    float
        Angular resolution in arcminutes
    """
    if nside <= 0:
        raise ValueError("nside must be positive")
    
    # Mean spacing between pixel centers
    return np.sqrt(3.0 / np.pi) * 180.0 * 60.0 / nside


def pixel_area(nside: int, units: str = "steradians") -> float:
    """
    Calculate the area of a HEALPix pixel.
    
    Parameters
    ----------
    nside : int
        HEALPix nside parameter
    units : str, optional
        Output units. Options: 'steradians', 'arcmin2', 'deg2'
        Default is 'steradians'
        
    Returns
    -------
    float
        Pixel area in the specified units
    """
    if nside <= 0:
        raise ValueError("nside must be positive")
    
    # Area in steradians
    area_sr = 4.0 * np.pi / (12 * nside**2)
    
    if units == "steradians":
        return area_sr
    elif units == "arcmin2":
        # Convert to square arcminutes
        return area_sr * (180.0 * 60.0 / np.pi)**2
    elif units == "deg2":
        # Convert to square degrees
        return area_sr * (180.0 / np.pi)**2
    else:
        raise ValueError(f"Unknown units: {units}")


def angular_distance(
    lon1: Union[float, np.ndarray],
    lat1: Union[float, np.ndarray], 
    lon2: Union[float, np.ndarray],
    lat2: Union[float, np.ndarray],
    units: str = "radians"
) -> Union[float, np.ndarray]:
    """
    Calculate angular distance between points on the sphere.
    
    Uses the haversine formula for accurate calculation of angular distances.
    
    Parameters
    ----------
    lon1, lat1 : float or array
        Longitude and latitude of first point(s)
    lon2, lat2 : float or array
        Longitude and latitude of second point(s)
    units : str, optional
        Input/output units. Options: 'radians', 'degrees'
        Default is 'radians'
        
    Returns
    -------
    float or array
        Angular distance(s) in the same units as input
    """
    # Convert to radians if needed
    if units == "degrees":
        lon1_rad = np.radians(lon1)
        lat1_rad = np.radians(lat1) 
        lon2_rad = np.radians(lon2)
        lat2_rad = np.radians(lat2)
    else:
        lon1_rad, lat1_rad = lon1, lat1
        lon2_rad, lat2_rad = lon2, lat2
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (np.sin(dlat/2)**2 + 
         np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2)
    
    distance_rad = 2 * np.arcsin(np.sqrt(a))
    
    # Convert back to original units if needed
    if units == "degrees":
        return np.degrees(distance_rad)
    else:
        return distance_rad


def cartesian_to_spherical(
    x: Union[float, np.ndarray],
    y: Union[float, np.ndarray],
    z: Union[float, np.ndarray]
) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Convert Cartesian coordinates to spherical coordinates.
    
    Parameters
    ----------
    x, y, z : float or array
        Cartesian coordinates
        
    Returns
    -------
    Tuple[float or array, float or array]
        Longitude and latitude in radians
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    
    # Avoid division by zero
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        lon = np.arctan2(y, x)
        lat = np.arcsin(z / r)
    
    # Handle points at origin
    if np.isscalar(r):
        if r == 0:
            return 0.0, 0.0
    else:
        mask = (r == 0)
        if np.any(mask):
            lon = np.where(mask, 0.0, lon)
            lat = np.where(mask, 0.0, lat)
    
    return lon, lat


def spherical_to_cartesian(
    lon: Union[float, np.ndarray],
    lat: Union[float, np.ndarray],
    r: Union[float, np.ndarray] = 1.0
) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Convert spherical coordinates to Cartesian coordinates.
    
    Parameters
    ----------
    lon, lat : float or array
        Longitude and latitude in radians
    r : float or array, optional
        Radial distance. Default is 1.0
        
    Returns
    -------
    Tuple[float or array, float or array, float or array]
        Cartesian coordinates (x, y, z)
    """
    x = r * np.cos(lat) * np.cos(lon)
    y = r * np.cos(lat) * np.sin(lon)
    z = r * np.sin(lat)
    
    return x, y, z


def deg2rad(degrees: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert degrees to radians."""
    return np.radians(degrees)


def rad2deg(radians: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert radians to degrees."""
    return np.degrees(radians)


def arcmin2rad(arcmin: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert arcminutes to radians."""
    return np.radians(arcmin / 60.0)


def rad2arcmin(radians: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert radians to arcminutes."""
    return np.degrees(radians) * 60.0


def arcsec2rad(arcsec: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert arcseconds to radians."""
    return np.radians(arcsec / 3600.0)


def rad2arcsec(radians: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert radians to arcseconds."""
    return np.degrees(radians) * 3600.0


def gaussian_beam(theta: Union[float, np.ndarray], fwhm: float) -> Union[float, np.ndarray]:
    """
    Calculate a Gaussian beam profile.
    
    Parameters
    ----------
    theta : float or array
        Angular distance from beam center in radians
    fwhm : float
        Full width at half maximum of the beam in radians
        
    Returns
    -------
    float or array
        Beam response (normalized to 1 at center)
    """
    sigma = fwhm / (2.0 * np.sqrt(2.0 * np.log(2.0)))
    return np.exp(-0.5 * (theta / sigma)**2)


def tophat_beam(theta: Union[float, np.ndarray], radius: float) -> Union[float, np.ndarray]:
    """
    Calculate a top-hat beam profile.
    
    Parameters
    ----------
    theta : float or array
        Angular distance from beam center in radians
    radius : float
        Beam radius in radians
        
    Returns
    -------
    float or array
        Beam response (1 inside radius, 0 outside)
    """
    return np.where(theta <= radius, 1.0, 0.0)


def planck_function(
    frequency: Union[float, np.ndarray],
    temperature: float
) -> Union[float, np.ndarray]:
    """
    Calculate the Planck function for black body radiation.
    
    Parameters
    ----------
    frequency : float or array
        Frequency in Hz
    temperature : float
        Temperature in Kelvin
        
    Returns
    -------
    float or array
        Planck function value in W m^-2 Hz^-1 sr^-1
    """
    # Physical constants
    h = 6.62607015e-34  # Planck constant (J⋅s)
    c = 299792458.0     # Speed of light (m/s)
    k_B = 1.380649e-23  # Boltzmann constant (J/K)
    
    # Calculate Planck function
    prefactor = 2.0 * h * frequency**3 / c**2
    exponential = np.expm1(h * frequency / (k_B * temperature))
    
    return prefactor / exponential


def cmb_to_brightness_temperature(
    intensity: Union[float, np.ndarray],
    frequency: float
) -> Union[float, np.ndarray]:
    """
    Convert CMB intensity to brightness temperature.
    
    Parameters
    ----------
    intensity : float or array
        Intensity in W m^-2 Hz^-1 sr^-1
    frequency : float
        Observation frequency in Hz
        
    Returns
    -------
    float or array
        Brightness temperature in Kelvin
    """
    # Physical constants
    h = 6.62607015e-34  # Planck constant (J⋅s)
    c = 299792458.0     # Speed of light (m/s)
    k_B = 1.380649e-23  # Boltzmann constant (J/K)
    
    # CMB temperature
    T_cmb = 2.7255  # K
    
    # Derivative of Planck function at CMB temperature
    x = h * frequency / (k_B * T_cmb)
    dB_dT = (2.0 * h * frequency**3 / c**2) * (x * np.exp(x) / (np.expm1(x)**2)) / T_cmb
    
    return intensity / dB_dT


def validate_nside(nside: int) -> bool:
    """
    Validate that nside is a valid HEALPix parameter.
    
    Parameters
    ----------
    nside : int
        HEALPix nside parameter
        
    Returns
    -------
    bool
        True if valid, False otherwise
    """
    if not isinstance(nside, int):
        return False
    
    if nside <= 0:
        return False
    
    # Check if nside is a power of 2
    return (nside & (nside - 1)) == 0


def get_valid_nside_values(max_nside: int = 8192) -> list:
    """
    Get a list of valid HEALPix nside values up to a maximum.
    
    Parameters
    ----------
    max_nside : int, optional
        Maximum nside value. Default is 8192
        
    Returns
    -------
    list
        List of valid nside values
    """
    nside_values = []
    nside = 1
    while nside <= max_nside:
        nside_values.append(nside)
        nside *= 2
    
    return nside_values