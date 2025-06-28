# run_data_generator.py
"""
Main executable script for the Test Data Generator.
This script initializes and runs the command-line interface.
"""
import sys
from data_generator import cli

if __name__ == "__main__":
    # This allows the script to be run directly, and for the data_generator package
    # to be found if the script is run from the project's root directory.
    # For a proper package installation, this might not be strictly necessary,
    # but it's helpful for development and direct execution.
    # import os
    # project_root = os.path.dirname(os.path.abspath(__file__))
    # if project_root not in sys.path:
    #     sys.path.insert(0, project_root)

    cli.main()