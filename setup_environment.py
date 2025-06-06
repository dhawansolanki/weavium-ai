#!/usr/bin/env python
"""
Script to set up the environment for the Autogen Agents Framework.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def create_directories():
    """Create necessary directories for the framework."""
    directories = [
        "./data",
        "./logs",
        "./config"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def install_dependencies(dev=False):
    """Install dependencies from requirements.txt."""
    requirements_file = "requirements-dev.txt" if dev else "requirements.txt"
    
    if not Path(requirements_file).exists():
        print(f"Error: {requirements_file} not found.")
        return False
    
    print(f"Installing dependencies from {requirements_file}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("Dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def setup_env_file():
    """Set up the .env file if it doesn't exist."""
    env_file = ".env"
    env_example_file = ".env.example"
    
    if Path(env_file).exists():
        print(f"{env_file} already exists. Skipping.")
        return
    
    if not Path(env_example_file).exists():
        print(f"Error: {env_example_file} not found.")
        return
    
    # Copy the example file to .env
    with open(env_example_file, "r") as example_file:
        example_content = example_file.read()
    
    with open(env_file, "w") as env_file_obj:
        env_file_obj.write(example_content)
    
    print(f"Created {env_file} from {env_example_file}.")
    print("Please update the .env file with your credentials.")

def make_scripts_executable():
    """Make scripts executable."""
    scripts = [
        "autogen-framework",
        "run_tests.py",
        "run_example.py"
    ]
    
    for script in scripts:
        if Path(script).exists():
            try:
                os.chmod(script, 0o755)
                print(f"Made {script} executable.")
            except Exception as e:
                print(f"Error making {script} executable: {e}")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Set up the environment for the Autogen Agents Framework")
    parser.add_argument("--dev", action="store_true", help="Install development dependencies")
    args = parser.parse_args()
    
    print("Setting up the environment for the Autogen Agents Framework...")
    
    # Create necessary directories
    create_directories()
    
    # Install dependencies
    install_dependencies(args.dev)
    
    # Set up the .env file
    setup_env_file()
    
    # Make scripts executable
    make_scripts_executable()
    
    print("\nEnvironment setup complete!")
    print("\nNext steps:")
    print("1. Update the .env file with your credentials")
    print("2. Run an example: python run_example.py basic_conversation")
    print("3. Run the tests: python run_tests.py")

if __name__ == "__main__":
    main()
