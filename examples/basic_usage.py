#!/usr/bin/env python3
"""
Basic example of using the expresso package.

This example demonstrates how to:
1. Create a random sky map
2. Compress it using different methods
3. Get compression statistics
4. Decompress and compare results
"""

import numpy as np
import expresso

def main():
    print("Expresso Package Example")
    print("=" * 50)
    
    # Create a random sky map for testing
    print("\n1. Creating a random sky map...")
    skymap = expresso.create_random_skymap(nside=64, seed=42)
    print(f"Created sky map: {skymap}")
    
    # Get basic statistics
    print("\n2. Computing sky map statistics...")
    stats = skymap.get_stats()
    print(f"Mean: {stats['mean']:.6e}")
    print(f"Std:  {stats['std']:.6e}")
    print(f"Min:  {stats['min']:.6e}")
    print(f"Max:  {stats['max']:.6e}")
    
    # Compress the sky map
    print("\n3. Compressing sky map...")
    compressed_data = expresso.compress_skymap(
        skymap.data, 
        method="wavelet", 
        compression_ratio=0.1
    )
    
    # Get compression info
    info = expresso.get_compression_info(compressed_data)
    print(f"Compression method: {info['method']}")
    print(f"Original size: {info['original_size_bytes']} bytes")
    print(f"Compressed size: {info['compressed_size_bytes']} bytes") 
    print(f"Compression ratio: {info['compression_ratio']:.3f}")
    print(f"Space saved: {info['space_saved_percent']:.1f}%")
    
    # Decompress
    print("\n4. Decompressing...")
    decompressed_data = expresso.decompress_skymap(compressed_data)
    
    # Compare original and decompressed
    print("\n5. Comparing original and decompressed data...")
    difference = skymap.data - decompressed_data
    print(f"Max absolute difference: {np.max(np.abs(difference)):.6e}")
    print(f"RMS difference: {np.sqrt(np.mean(difference**2)):.6e}")
    
    # Test different compression ratios
    print("\n6. Testing different compression ratios...")
    ratios = [0.01, 0.05, 0.1, 0.2, 0.5]
    
    for ratio in ratios:
        compressed = expresso.compress_skymap(skymap.data, compression_ratio=ratio)
        decompressed = expresso.decompress_skymap(compressed)
        
        # Calculate reconstruction error
        error = np.sqrt(np.mean((skymap.data - decompressed)**2))
        
        info = expresso.get_compression_info(compressed)
        print(f"Ratio {ratio:4.2f}: {info['space_saved_percent']:5.1f}% saved, "
              f"RMS error: {error:.6e}")
    
    print("\nExample completed successfully!")


if __name__ == "__main__":
    main()