# data_generator/engine.py
"""
Core data generation engine.
Takes a parsed schema and generates a single data record.
"""
from .value_generators import dispatch_generator
from .exceptions import GeneratorError


def generate_single_record(parsed_node, base_dir):
    """
    Generates a single data record based on a parsed schema node.

    Args:
        parsed_node: A node from the schema after parsing by schema_parser.py.
                     This can be a dictionary representing a parsed directive,
                     a dictionary representing a nested object schema,
                     or a literal value.
        base_dir: The base directory for resolving relative paths, primarily for
                  array:object sub-schemas. This should be the directory of the
                  schema file from which `parsed_node`'s structure originated.

    Returns:
        The generated data corresponding to the parsed_node.
    """
    if isinstance(parsed_node, dict):
        # Check if it's a fully parsed directive object (leaf node for generation)
        if "data_type" in parsed_node and "generator_name" in parsed_node:
            try:
                return dispatch_generator(parsed_node, base_dir)
            except GeneratorError as e:
                directive_str = parsed_node.get('original_directive', 'unknown directive')
                raise GeneratorError(f"Error generating value for directive '{directive_str}': {e}")
            except Exception as e:
                directive_str = parsed_node.get('original_directive', 'unknown directive')
                raise GeneratorError(f"Unexpected error processing directive '{directive_str}': {e}")

        # Otherwise, it's a nested object schema. Iterate through its keys.
        else:
            record_part = {}
            for key, sub_node in parsed_node.items():
                try:
                    record_part[key] = generate_single_record(sub_node, base_dir)
                except GeneratorError as e:
                    raise GeneratorError(f"Error generating field '{key}': {e}")
                except Exception as e:
                    raise GeneratorError(f"Unexpected error generating field '{key}': {e}")
            return record_part

    elif isinstance(parsed_node, list):
        # If the schema itself contains a list of items to be processed
        return [generate_single_record(item, base_dir) for item in parsed_node]

    else:
        # It's a literal value (e.g., a string not matching a directive, a number, boolean, null)
        return parsed_node

