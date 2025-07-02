# data_generator/cli.py
"""
Command-Line Interface (CLI) for the JGenPy.
"""
import argparse
import json
import os
import sys
from .schema_parser import parse_schema_from_file
from .engine import generate_single_record
from .output import write_output
from .exceptions import DataGeneratorError, FileHandlingError


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

    try:
        # Get the directory of the main schema file to resolve relative paths for sub-schemas
        base_dir = os.path.dirname(os.path.abspath(args.schema_file))

        parsed_schema = parse_schema_from_file(args.schema_file, base_dir)

        generated_data = []
        for i in range(args.num_records):
            # Visual feedback for long generation times
            if args.num_records > 100 and (i + 1) % (args.num_records // 10) == 0:
                print(f"Generating record {i + 1}/{args.num_records}...", file=sys.stderr)

            record = generate_single_record(parsed_schema, base_dir)
            generated_data.append(record)

        write_output(generated_data, args.output)
        if args.output:
            print(f"Successfully generated {args.num_records} records to {args.output}", file=sys.stderr)
        else:
            # If printing to stdout, a final confirmation might be redundant if data is large
            print(f"\nSuccessfully generated {args.num_records} records.", file=sys.stderr)


    except DataGeneratorError as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from schema file '{args.schema_file}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
