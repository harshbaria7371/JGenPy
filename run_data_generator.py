# run_data_generator.py
"""
Main executable script for the JGenPy.
This script initializes and runs the command-line interface.
"""
import sys
from data_generator import cli

if __name__ == "__main__":
    # This allows the script to be run directly, and for the data_generator package
    cli.main()