# data_generator/schema_parser.py
"""
Parses the input JSON schema and extracts data generation directives.
Handles nested schemas and relative path resolution for sub-schemas.
"""
import json
import os
import re
from .exceptions import InvalidSchemaError, DirectiveError, FileHandlingError

# Regex to parse generator parameters like (key=value, key2=value2)
PARAMS_REGEX = re.compile(r"\((.*)\)")


def _parse_directive_params(param_string):
    """
    Parses a parameter string like "key1=value1,key2=value2" into a dictionary.
    """
    if not param_string:
        return {}

    params = {}
    # This is a simplified parser. It splits by comma but won't handle commas within values
    format_match = re.search(r"format=([^,]+)", param_string)
    if format_match:
        format_val = format_match.group(1)
        params['format'] = format_val
        # Remove the format part before splitting the rest by comma
        param_string = param_string.replace(format_match.group(0), '')

    param_pairs = param_string.split(',')

    for pair in param_pairs:
        if '=' not in pair:
            continue

        key, value_str = pair.split('=', 1)
        key = key.strip()
        value_str = value_str.strip()

        if not key: continue

        # Attempt to convert to int, float, or bool if appropriate
        if value_str.lower() == 'true':
            params[key] = True
        elif value_str.lower() == 'false':
            params[key] = False
        elif (value_str.startswith("'") and value_str.endswith("'")) or \
                (value_str.startswith('"') and value_str.endswith('"')):
            params[key] = value_str[1:-1]
        else:
            try:
                params[key] = int(value_str)
            except ValueError:
                try:
                    params[key] = float(value_str)
                except ValueError:
                    params[key] = value_str  # Keep as string
    return params


def _parse_directive_string(directive_str, base_dir):
    """
    Parses a directive string like "datatype:generator_name(params)"
    """
    if ':' not in directive_str:
        raise DirectiveError(f"Invalid directive format: '{directive_str}'. Expected 'datatype:details'.")

    # Split only on the first colon to separate the main data type
    parts = directive_str.split(':', 1)
    data_type = parts[0]
    details = parts[1]

    parsed_directive = {"original_directive": directive_str, "data_type": data_type}

    if data_type == "array":
        # Array directives have a second colon: array:type:details
        if ':' not in details:
            raise DirectiveError(
                f"Invalid array directive format: '{directive_str}'. Expected 'array:primitive_type_or_object:details'.")

        array_parts = details.split(':', 1)
        array_content_type = array_parts[0]
        array_details_spec = array_parts[1]

        # For primitive arrays, we need to separate array-level params (like count)
        # from the element generator spec (like range(min=1,max=5))
        # The format is: generator_spec,count=N or generator_spec
        params = {}
        sub_generator_str = array_details_spec
        
        # Look for array-level parameters at the end (like count=3)
        # These come after the generator spec, separated by comma
        # We need to be careful not to split on commas inside parentheses
        count_match = re.search(r',\s*count\s*=\s*(\d+)', array_details_spec)
        if count_match:
            params['count'] = int(count_match.group(1))
            # Remove the count parameter from the string
            sub_generator_str = array_details_spec[:count_match.start()].rstrip(', ')
        
        parsed_directive["params"] = params

        if array_content_type == "object":
            parsed_directive["generator_name"] = "object_array"
            if "schema_file" not in params:
                raise DirectiveError(f"Missing 'schema_file' for array:object directive: '{directive_str}'")
            if "count" not in params:
                raise DirectiveError(f"Missing 'count' for array:object directive: '{directive_str}'")

            relative_path = params["schema_file"]
            absolute_path = os.path.join(base_dir, relative_path)

            if not os.path.exists(absolute_path):
                raise FileHandlingError(f"Sub-schema file not found: '{absolute_path}'")

            sub_schema_base_dir = os.path.dirname(absolute_path)
            params["parsed_sub_schema"] = parse_schema_from_file(absolute_path, sub_schema_base_dir)

        elif array_content_type in ["string", "integer", "float", "boolean"]:
            parsed_directive["generator_name"] = "primitive_array"
            params["element_type"] = array_content_type
            if "count" not in params:
                raise DirectiveError(f"Missing 'count' for primitive array directive: '{directive_str}'")

            element_directive_str = f"{array_content_type}:{sub_generator_str}"
            params["element_generator_details"] = _parse_directive_string(element_directive_str, base_dir)
        else:
            raise DirectiveError(
                f"Unsupported array content type '{array_content_type}' in directive: '{directive_str}'")

    elif data_type in ["string", "integer", "float", "boolean", "date"]:
        generator_full_spec = details
        param_match = PARAMS_REGEX.search(generator_full_spec)

        if param_match:
            parsed_directive["generator_name"] = generator_full_spec[:param_match.start()]
            param_string = param_match.group(1)
            parsed_directive["params"] = _parse_directive_params(param_string)
        else:
            parsed_directive["generator_name"] = generator_full_spec
            parsed_directive["params"] = {}
    else:
        raise DirectiveError(f"Unsupported data type '{data_type}' in directive: '{directive_str}'")

    return parsed_directive


def _process_schema_node(node, base_dir):
    """
    Recursively processes a node in the schema.
    """
    if isinstance(node, str):
        if ':' in node:
            try:
                return _parse_directive_string(node, base_dir)
            except DirectiveError:
                # If parsing fails, assume it's a literal string
                return node
        else:
            return node  # Literal string
    elif isinstance(node, dict):
        return {key: _process_schema_node(value, base_dir) for key, value in node.items()}
    elif isinstance(node, list):
        return [_process_schema_node(item, base_dir) for item in node]
    else:
        # Literal value (number, boolean, null)
        return node


def parse_schema_from_file(schema_file_path, base_dir):
    """
    Loads a JSON schema from a file and processes it to parse all directives.
    """
    try:
        with open(schema_file_path, 'r', encoding='utf-8') as f:
            raw_schema = json.load(f)
    except FileNotFoundError:
        raise FileHandlingError(f"Schema file not found: {schema_file_path}")
    except json.JSONDecodeError as e:
        raise InvalidSchemaError(f"Invalid JSON in schema file {schema_file_path}: {e}")

    if not isinstance(raw_schema, dict):
        raise InvalidSchemaError("Root of the schema must be a JSON object.")

    return _process_schema_node(raw_schema, base_dir)