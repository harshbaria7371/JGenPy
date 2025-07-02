# data_generator/output.py
"""
Handles the output of generated test data.
It generates specified JSON file in output file path.
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
            sys.stdout.write('\n')
        except Exception as e:
            print(f"Error writing to stdout: {e}", file=sys.stderr)

