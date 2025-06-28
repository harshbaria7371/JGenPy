# data_generator/output.py
"""
Handles the output of generated test data.
Can output to stdout (console) or to a specified JSON file.
"""
import json
import sys
import os
from .exceptions import FileHandlingError


def write_output(data_records, output_file_path=None):
    """
    Writes the list of generated data records to the specified output.

    Args:
        data_records (list): A list of dictionaries, where each dictionary
                             is a generated data record.
        output_file_path (str, optional): Path to the output JSON file.
                                          If None, output is printed to stdout.

    Raises:
        FileHandlingError: If there's an issue writing to the output file.
    """
    if output_file_path:
        try:
            directory = os.path.dirname(output_file_path)

            if directory:
                os.makedirs(directory, exist_ok=True)

            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(data_records, f, indent=2, ensure_ascii=False)

        except IOError as e:
            raise FileHandlingError(f"Error writing to output file {output_file_path}: {e}")
        except Exception as e:
            raise FileHandlingError(f"An unexpected error occurred while writing to {output_file_path}: {e}")
    else:
        # Print to stdout
        try:
            json.dump(data_records, sys.stdout, indent=2, ensure_ascii=False)
            sys.stdout.write('\n')  # Add a newline after the JSON output
        except Exception as e:
            # This might happen if stdout is closed or similar, though less common.
            # We can't use FileHandlingError here as it's not a typical file.
            print(f"Error writing to stdout: {e}", file=sys.stderr)

