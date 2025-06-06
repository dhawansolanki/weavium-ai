#!/usr/bin/env python
"""
Script to run examples from the Autogen Agents Framework.
"""

import os
import sys
import argparse
import runpy
from pathlib import Path

def list_examples():
    """List all available examples."""
    examples_dir = Path(__file__).parent / "examples"
    examples = [f.stem for f in examples_dir.glob("*.py") if f.is_file()]
    return sorted(examples)

def run_example(example_name):
    """
    Run the specified example.
    
    Args:
        example_name: Name of the example to run
    """
    # Check if the example exists
    example_path = Path(__file__).parent / "examples" / f"{example_name}.py"
    if not example_path.exists():
        print(f"Error: Example '{example_name}' not found.")
        print("Available examples:")
        for example in list_examples():
            print(f"  - {example}")
        return 1
    
    # Add the parent directory to the Python path
    sys.path.append(str(Path(__file__).parent))
    
    # Run the example
    print(f"Running example: {example_name}")
    print("-" * 80)
    
    # Run the example script directly
    try:
        # Use runpy to execute the script
        runpy.run_path(str(example_path), run_name="__main__")
    except Exception as e:
        print(f"Error running example '{example_name}': {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run examples from the Autogen Agents Framework")
    parser.add_argument("example", nargs="?", help="Name of the example to run")
    parser.add_argument("--list", "-l", action="store_true", help="List all available examples")
    args = parser.parse_args()
    
    # List examples if requested
    if args.list:
        print("Available examples:")
        for example in list_examples():
            print(f"  - {example}")
        sys.exit(0)
    
    # Check if an example was specified
    if not args.example:
        parser.print_help()
        print("\nAvailable examples:")
        for example in list_examples():
            print(f"  - {example}")
        sys.exit(1)
    
    # Run the specified example
    sys.exit(run_example(args.example))
