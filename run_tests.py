#!/usr/bin/env python
"""
Script to run all tests for the Autogen Agents Framework.
"""

import os
import sys
import unittest
import argparse
from pathlib import Path

def run_tests(test_path=None, verbose=False):
    """
    Run all tests in the specified path.
    
    Args:
        test_path: Path to the test directory or file
        verbose: Whether to show verbose output
    """
    # Set up the test loader
    loader = unittest.TestLoader()
    
    # Determine the test path
    if test_path is None:
        test_path = os.path.join(os.path.dirname(__file__), "tests")
    
    # Discover and run tests
    suite = loader.discover(test_path)
    
    # Set up the test runner
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    
    # Run the tests
    result = runner.run(suite)
    
    # Return the exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run tests for the Autogen Agents Framework")
    parser.add_argument("--path", help="Path to the test directory or file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose output")
    args = parser.parse_args()
    
    # Run the tests
    sys.exit(run_tests(args.path, args.verbose))
