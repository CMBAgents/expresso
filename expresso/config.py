"""
Configuration management for the expresso package.

This module provides configuration handling, default settings, and
parameter validation for various package components.
"""

import os
from typing import Dict, Any, Optional, Union
import warnings
import json


class ConfigError(Exception):
    """Exception raised for configuration-related errors."""
    pass


# Default configuration values
DEFAULT_CONFIG = {
    "compression": {
        "default_method": "wavelet",
        "default_ratio": 0.1,
        "allowed_methods": ["wavelet", "pca", "svd"],
        "max_ratio": 0.9,
        "min_ratio": 0.001
    },
    "skymap": {
        "default_nside": 64,
        "default_coordinate_system": "galactic",
        "default_units": "unknown",
        "max_nside": 8192,
        "valid_coordinate_systems": ["galactic", "equatorial", "ecliptic"]
    },
    "io": {
        "default_format": "fits",
        "supported_formats": ["fits", "healpix", "numpy", "numpy_compressed"],
        "default_overwrite": False,
        "max_file_size_mb": 1000
    },
    "utils": {
        "default_angle_units": "radians",
        "default_beam_type": "gaussian",
        "cmb_temperature": 2.7255  # Kelvin
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
}


class Config:
    """
    Configuration manager for expresso package.
    
    This class handles loading, saving, and accessing configuration
    parameters for the package.
    """
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.
        
        Parameters
        ----------
        config_dict : Dict[str, Any], optional
            Configuration dictionary. If None, uses default config.
        """
        if config_dict is None:
            self._config = DEFAULT_CONFIG.copy()
        else:
            self._config = self._merge_configs(DEFAULT_CONFIG, config_dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Parameters
        ----------
        key : str
            Configuration key (can use dot notation, e.g., 'compression.default_method')
        default : Any, optional
            Default value if key is not found
            
        Returns
        -------
        Any
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Parameters
        ----------
        key : str
            Configuration key (can use dot notation)
        value : Any
            Value to set
        """
        keys = key.split('.')
        config = self._config
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        Update configuration with values from a dictionary.
        
        Parameters
        ----------
        config_dict : Dict[str, Any]
            Dictionary with configuration updates
        """
        self._config = self._merge_configs(self._config, config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get the full configuration as a dictionary.
        
        Returns
        -------
        Dict[str, Any]
            Complete configuration dictionary
        """
        return self._config.copy()
    
    def save(self, filename: str) -> None:
        """
        Save configuration to a JSON file.
        
        Parameters
        ----------
        filename : str
            Output filename
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            raise ConfigError(f"Failed to save config to {filename}: {e}")
    
    @classmethod
    def load(cls, filename: str) -> "Config":
        """
        Load configuration from a JSON file.
        
        Parameters
        ----------
        filename : str
            Configuration file to load
            
        Returns
        -------
        Config
            Configuration object
        """
        try:
            with open(filename, 'r') as f:
                config_dict = json.load(f)
            return cls(config_dict)
        except Exception as e:
            raise ConfigError(f"Failed to load config from {filename}: {e}")
    
    def validate(self) -> bool:
        """
        Validate the current configuration.
        
        Returns
        -------
        bool
            True if configuration is valid
            
        Raises
        ------
        ConfigError
            If configuration is invalid
        """
        # Validate compression settings
        comp_method = self.get('compression.default_method')
        allowed_methods = self.get('compression.allowed_methods', [])
        if comp_method not in allowed_methods:
            raise ConfigError(f"Invalid compression method: {comp_method}")
        
        ratio = self.get('compression.default_ratio')
        min_ratio = self.get('compression.min_ratio', 0)
        max_ratio = self.get('compression.max_ratio', 1)
        if not min_ratio <= ratio <= max_ratio:
            raise ConfigError(f"Compression ratio {ratio} out of range [{min_ratio}, {max_ratio}]")
        
        # Validate skymap settings
        nside = self.get('skymap.default_nside')
        if nside <= 0 or (nside & (nside - 1)) != 0:
            raise ConfigError(f"Invalid nside value: {nside} (must be positive power of 2)")
        
        coord_sys = self.get('skymap.default_coordinate_system')
        valid_coords = self.get('skymap.valid_coordinate_systems', [])
        if coord_sys not in valid_coords:
            raise ConfigError(f"Invalid coordinate system: {coord_sys}")
        
        return True
    
    def _merge_configs(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge two configuration dictionaries."""
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result


# Global configuration instance
_global_config = Config()


def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns
    -------
    Config
        Global configuration object
    """
    return _global_config


def set_config(config: Union[Config, Dict[str, Any]]) -> None:
    """
    Set the global configuration.
    
    Parameters
    ----------
    config : Config or Dict[str, Any]
        New configuration
    """
    global _global_config
    
    if isinstance(config, Config):
        _global_config = config
    else:
        _global_config = Config(config)


def load_config_file(filename: str) -> None:
    """
    Load configuration from file and set as global config.
    
    Parameters
    ----------
    filename : str
        Configuration file to load
    """
    config = Config.load(filename)
    set_config(config)


def save_config_file(filename: str) -> None:
    """
    Save current global configuration to file.
    
    Parameters
    ----------
    filename : str
        Output filename
    """
    _global_config.save(filename)


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get a configuration value from global config.
    
    Parameters
    ----------
    key : str
        Configuration key
    default : Any, optional
        Default value if key not found
        
    Returns
    -------
    Any
        Configuration value
    """
    return _global_config.get(key, default)


def set_config_value(key: str, value: Any) -> None:
    """
    Set a configuration value in global config.
    
    Parameters
    ----------
    key : str
        Configuration key
    value : Any
        Value to set
    """
    _global_config.set(key, value)


def reset_config() -> None:
    """Reset global configuration to defaults."""
    global _global_config
    _global_config = Config()


def get_user_config_dir() -> str:
    """
    Get the user configuration directory for expresso.
    
    Returns
    -------
    str
        Path to user configuration directory
    """
    # Use XDG standard on Unix-like systems
    if os.name == 'posix':
        config_home = os.environ.get('XDG_CONFIG_HOME', 
                                   os.path.expanduser('~/.config'))
        return os.path.join(config_home, 'expresso')
    else:
        # Use AppData on Windows
        return os.path.join(os.path.expanduser('~'), '.expresso')


def load_user_config() -> None:
    """
    Load user configuration from default location if it exists.
    """
    config_dir = get_user_config_dir()
    config_file = os.path.join(config_dir, 'config.json')
    
    if os.path.exists(config_file):
        try:
            load_config_file(config_file)
        except Exception as e:
            warnings.warn(f"Failed to load user config: {e}", UserWarning)


def save_user_config() -> None:
    """
    Save current configuration to user config directory.
    """
    config_dir = get_user_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    
    config_file = os.path.join(config_dir, 'config.json')
    save_config_file(config_file)


# Try to load user config on import
try:
    load_user_config()
except Exception:
    # Silently ignore errors during module import
    pass