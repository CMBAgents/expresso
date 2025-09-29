"""
Command-line interface for the expresso package.

This module provides command-line tools for compressing sky maps,
processing astronomical data, and other package functionality.
"""

import argparse
import sys
from typing import Optional, List
import warnings

from . import __version__
from .compression import compress_skymap, decompress_skymap, get_compression_info
from .skymap import load_skymap, save_skymap, create_random_skymap
from .config import get_config_value, set_config_value, save_user_config


def create_parser() -> argparse.ArgumentParser:
    """
    Create the main argument parser.
    
    Returns
    -------
    argparse.ArgumentParser
        Main parser with all subcommands
    """
    parser = argparse.ArgumentParser(
        description="Expresso: Tools to compress and express information from maps of the sky",
        prog="expresso"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"expresso {__version__}"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )
    
    # Compression commands
    compress_parser = subparsers.add_parser(
        "compress",
        help="Compress a sky map"
    )
    compress_parser.add_argument(
        "input",
        help="Input sky map file"
    )
    compress_parser.add_argument(
        "output", 
        help="Output compressed file"
    )
    compress_parser.add_argument(
        "--method", "-m",
        choices=["wavelet", "pca", "svd"],
        default="wavelet",
        help="Compression method (default: wavelet)"
    )
    compress_parser.add_argument(
        "--ratio", "-r",
        type=float,
        default=0.1,
        help="Compression ratio (default: 0.1)"
    )
    
    # Decompression commands
    decompress_parser = subparsers.add_parser(
        "decompress",
        help="Decompress a sky map"
    )
    decompress_parser.add_argument(
        "input",
        help="Input compressed file"
    )
    decompress_parser.add_argument(
        "output",
        help="Output sky map file"
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Get information about a compressed file"
    )
    info_parser.add_argument(
        "input",
        help="Input compressed file"
    )
    
    # Stats command
    stats_parser = subparsers.add_parser(
        "stats",
        help="Get statistics about a sky map"
    )
    stats_parser.add_argument(
        "input",
        help="Input sky map file"
    )
    
    # Generate command
    generate_parser = subparsers.add_parser(
        "generate", 
        help="Generate a random sky map for testing"
    )
    generate_parser.add_argument(
        "output",
        help="Output sky map file"
    )
    generate_parser.add_argument(
        "--nside",
        type=int,
        default=64,
        help="HEALPix nside parameter (default: 64)"
    )
    generate_parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility"
    )
    
    # Config commands
    config_parser = subparsers.add_parser(
        "config",
        help="Configuration management"
    )
    config_subparsers = config_parser.add_subparsers(
        dest="config_command",
        help="Configuration commands"
    )
    
    # Config get
    config_get_parser = config_subparsers.add_parser(
        "get",
        help="Get configuration value"
    )
    config_get_parser.add_argument(
        "key",
        help="Configuration key (e.g., compression.default_method)"
    )
    
    # Config set
    config_set_parser = config_subparsers.add_parser(
        "set",
        help="Set configuration value"
    )
    config_set_parser.add_argument(
        "key",
        help="Configuration key"
    )
    config_set_parser.add_argument(
        "value",
        help="Configuration value"
    )
    
    # Config save
    config_subparsers.add_parser(
        "save",
        help="Save current configuration to user config"
    )
    
    return parser


def cmd_compress(args: argparse.Namespace) -> int:
    """Handle compress command."""
    try:
        print(f"Loading sky map from {args.input}...")
        skymap = load_skymap(args.input)
        
        print(f"Compressing with method '{args.method}' and ratio {args.ratio}...")
        compressed_data = compress_skymap(
            skymap.data,
            method=args.method,
            compression_ratio=args.ratio
        )
        
        # Save compressed data (would use appropriate format)
        import pickle
        with open(args.output, 'wb') as f:
            pickle.dump(compressed_data, f)
        
        # Show compression info
        info = get_compression_info(compressed_data)
        print(f"Compression complete:")
        print(f"  Original size: {info['original_size_bytes']} bytes")
        print(f"  Compressed size: {info['compressed_size_bytes']} bytes")
        print(f"  Compression ratio: {info['compression_ratio']:.3f}")
        print(f"  Space saved: {info['space_saved_percent']:.1f}%")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_decompress(args: argparse.Namespace) -> int:
    """Handle decompress command."""
    try:
        print(f"Loading compressed data from {args.input}...")
        
        # Load compressed data
        import pickle
        with open(args.input, 'rb') as f:
            compressed_data = pickle.load(f)
        
        print("Decompressing...")
        data = decompress_skymap(compressed_data)
        
        # Create skymap object and save
        from .skymap import SkyMap
        skymap = SkyMap(data)
        save_skymap(skymap, args.output)
        
        print(f"Decompression complete. Saved to {args.output}")
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_info(args: argparse.Namespace) -> int:
    """Handle info command."""
    try:
        # Load compressed data
        import pickle
        with open(args.input, 'rb') as f:
            compressed_data = pickle.load(f)
        
        info = get_compression_info(compressed_data)
        
        print(f"Compression Information:")
        print(f"  Method: {info['method']}")
        print(f"  Original size: {info['original_size_bytes']} bytes")
        print(f"  Compressed size: {info['compressed_size_bytes']} bytes")
        print(f"  Compression ratio: {info['compression_ratio']:.3f}")
        print(f"  Space saved: {info['space_saved_percent']:.1f}%")
        if info['shape']:
            print(f"  Original shape: {info['shape']}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_stats(args: argparse.Namespace) -> int:
    """Handle stats command."""
    try:
        print(f"Loading sky map from {args.input}...")
        skymap = load_skymap(args.input)
        
        stats = skymap.get_stats()
        
        print(f"Sky Map Statistics:")
        print(f"  Shape: {skymap.shape}")
        print(f"  Total pixels: {stats['total_pixels']}")
        print(f"  Valid pixels: {stats['valid_pixels']}")
        print(f"  Mean: {stats['mean']:.6e}")
        print(f"  Std: {stats['std']:.6e}")
        print(f"  Min: {stats['min']:.6e}")
        print(f"  Max: {stats['max']:.6e}")
        print(f"  Median: {stats['median']:.6e}")
        
        if skymap.nside:
            print(f"  HEALPix nside: {skymap.nside}")
            print(f"  Resolution: {skymap.resolution:.2f} arcmin")
        
        print(f"  Coordinate system: {skymap.coordinate_system}")
        print(f"  Units: {skymap.units}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_generate(args: argparse.Namespace) -> int:
    """Handle generate command."""
    try:
        print(f"Generating random sky map with nside={args.nside}...")
        
        skymap = create_random_skymap(
            nside=args.nside,
            seed=args.seed
        )
        
        save_skymap(skymap, args.output)
        
        print(f"Random sky map saved to {args.output}")
        print(f"  Shape: {skymap.shape}")
        print(f"  nside: {skymap.nside}")
        if args.seed:
            print(f"  Seed: {args.seed}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_config(args: argparse.Namespace) -> int:
    """Handle config commands."""
    try:
        if args.config_command == "get":
            value = get_config_value(args.key)
            if value is not None:
                print(f"{args.key} = {value}")
            else:
                print(f"Configuration key '{args.key}' not found")
                return 1
                
        elif args.config_command == "set":
            # Try to parse value as different types
            value = args.value
            try:
                # Try int
                value = int(value)
            except ValueError:
                try:
                    # Try float
                    value = float(value)
                except ValueError:
                    # Try bool
                    if value.lower() in ('true', 'yes', '1'):
                        value = True
                    elif value.lower() in ('false', 'no', '0'):
                        value = False
                    # Otherwise keep as string
            
            set_config_value(args.key, value)
            print(f"Set {args.key} = {value}")
            
        elif args.config_command == "save":
            save_user_config()
            print("Configuration saved to user config")
            
        else:
            print("No config command specified", file=sys.stderr)
            return 1
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Parameters
    ----------
    argv : List[str], optional
        Command line arguments. If None, uses sys.argv
        
    Returns
    -------
    int
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    
    if argv is None:
        argv = sys.argv[1:]
    
    args = parser.parse_args(argv)
    
    # Set verbosity
    if args.verbose:
        warnings.simplefilter("always")
    
    # Handle commands
    if args.command == "compress":
        return cmd_compress(args)
    elif args.command == "decompress":
        return cmd_decompress(args)
    elif args.command == "info":
        return cmd_info(args)
    elif args.command == "stats":
        return cmd_stats(args)
    elif args.command == "generate":
        return cmd_generate(args)
    elif args.command == "config":
        return cmd_config(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())