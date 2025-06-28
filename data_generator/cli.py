# data_generator/cli.py
"""
Command-Line Interface (CLI) for the JGenPy project.
Uses argparse to handle command-line arguments and orchestrates
the data generation process.
"""
import argparse
import json
import os
import sys


def main():
    """
    Main function to run the CLI.
    Parses arguments, loads schema, generates data, and handles output.
    """
    parser = argparse.ArgumentParser(
        description="Generate test data based on a JSON schema with embedded directives.",
        formatter_class=argparse.RawTextHelpFormatter  # To allow for better formatting in help
    )
    parser.add_argument(
        "schema_file",
        type=str,
        help="Path to the input JSON schema file."
    )
    parser.add_argument(
        "num_records",
        type=int,
        help="Number of data records to generate."
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Optional path for the output JSON file. Defaults to stdout."
    )

    args = parser.parse_args()

    if not os.path.exists(args.schema_file):
        print(f"Error: Schema file not found at {args.schema_file}", file=sys.stderr)
        sys.exit(1)

    if args.num_records <= 0:
        print("Error: Number of records must be a positive integer.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    # This allows running cli.py directly for testing,
    # though run_data_generator.py is the intended entry point.
    main()
