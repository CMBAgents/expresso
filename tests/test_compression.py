"""
Tests for the compression module.
"""

import pytest
import numpy as np
from expresso.compression import (
    compress_skymap, decompress_skymap, get_compression_info, 
    CompressionError
)


class TestCompression:
    """Test suite for compression functionality."""
    
    def test_compress_skymap_basic(self):
        """Test basic compression functionality."""
        # Create test data
        data = np.random.normal(0, 1, 1000)
        
        # Compress
        compressed = compress_skymap(data, method="wavelet", compression_ratio=0.1)
        
        # Check structure
        assert isinstance(compressed, dict)
        assert "method" in compressed
        assert "shape" in compressed
        assert "indices" in compressed
        assert "values" in compressed
        assert compressed["method"] == "wavelet"
        assert compressed["shape"] == data.shape
    
    def test_decompress_skymap_basic(self):
        """Test basic decompression functionality."""
        # Create and compress test data
        data = np.random.normal(0, 1, 1000)
        compressed = compress_skymap(data, method="wavelet", compression_ratio=0.1)
        
        # Decompress
        decompressed = decompress_skymap(compressed)
        
        # Check shape
        assert decompressed.shape == data.shape
        assert isinstance(decompressed, np.ndarray)
    
    def test_compression_ratio_validation(self):
        """Test compression ratio validation."""
        data = np.random.normal(0, 1, 100)
        
        # Test invalid ratios
        with pytest.raises(CompressionError):
            compress_skymap(data, compression_ratio=0.0)
        
        with pytest.raises(CompressionError):
            compress_skymap(data, compression_ratio=1.0)
        
        with pytest.raises(CompressionError):
            compress_skymap(data, compression_ratio=-0.1)
    
    def test_invalid_input_type(self):
        """Test handling of invalid input types."""
        with pytest.raises(CompressionError):
            compress_skymap([1, 2, 3], method="wavelet")
    
    def test_unknown_method(self):
        """Test handling of unknown compression methods."""
        data = np.random.normal(0, 1, 100)
        
        with pytest.raises(CompressionError):
            compress_skymap(data, method="unknown")
    
    def test_get_compression_info(self):
        """Test compression info function."""
        data = np.random.normal(0, 1, 1000)
        compressed = compress_skymap(data, method="wavelet", compression_ratio=0.1)
        
        info = get_compression_info(compressed)
        
        assert isinstance(info, dict)
        assert "method" in info
        assert "compression_ratio" in info
        assert "space_saved_percent" in info
        assert info["method"] == "wavelet"
        assert 0 <= info["compression_ratio"] <= 1
        assert 0 <= info["space_saved_percent"] <= 100


if __name__ == "__main__":
    pytest.main([__file__])