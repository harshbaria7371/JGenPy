# data_generator/value_generators.py
"""
Contains functions to generate specific data values based on parsed directives.
Uses the Faker library for generating realistic fake data.
"""
import random
import uuid
import os
import threading
from datetime import datetime, timedelta, timezone
from faker import Faker
import exrex  # For regex string generation
from .exceptions import GeneratorError, DirectiveError
from .config import get_configured_locale, get_country_from_config

# Initialize Faker with the locale from .config file
_configured_locale = get_configured_locale()
fake = Faker(_configured_locale)

# Thread-local storage for maintaining state across field generations in the same record
_thread_local = threading.local()

def _get_required_param(params, param_name, directive_str):
    """Helper to get a required parameter or raise GeneratorError."""
    if param_name not in params:
        raise GeneratorError(f"Missing required parameter '{param_name}' for directive '{directive_str}'")
    return params[param_name]


def _get_optional_param(params, param_name, default_value):
    """Helper to get an optional parameter."""
    return params.get(param_name, default_value)


# --- String Generators ---
def generate_string_email(**kwargs):
    return fake.email()

def generate_string_name(**kwargs):
    return fake.name()

def generate_string_phone(**kwargs):
    return fake.phone_number()

def generate_string_firstname(**kwargs):
    return fake.first_name()

def generate_string_lastname(**kwargs):
    return fake.last_name()

def generate_string_uuid(**kwargs):
    return str(uuid.uuid4())

def generate_string_lorem(params, directive_str, **kwargs):
    lorem_type = _get_optional_param(params, "type", "paragraph")
    if lorem_type == "paragraph":
        return fake.paragraph()
    elif lorem_type == "paragraphs":
        count = _get_optional_param(params, "count", 1)
        if not isinstance(count, int) or count <= 0:
            raise GeneratorError(f"Invalid 'count' for lorem(type=paragraphs): {count} in '{directive_str}'")
        return "\n\n".join(fake.paragraphs(nb=count))
    elif lorem_type == "sentence":
        return fake.sentence()
    elif lorem_type == "text":
        max_nb_chars = _get_optional_param(params, "max_nb_chars", 200)
        return fake.text(max_nb_chars=max_nb_chars)
    else:
        raise GeneratorError(f"Unknown lorem type '{lorem_type}' in directive '{directive_str}'")

def generate_string_word(**kwargs):
    return fake.word()

def generate_string_street_address(**kwargs):
    return fake.street_address()

def generate_string_vat_number(params, directive_str, **kwargs):   
    length = _get_required_param(params, "length", "string:vat_number")
    if not isinstance(length, int) or length <= 0:
        raise GeneratorError(f"Invalid 'length' for string:vat_number: {length} in '{directive_str}'")
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(characters) for _ in range(length))

def generate_string_city(**kwargs):
    return fake.city()

def generate_string_country(**kwargs):
    try:
        return get_country_from_config()
    except Exception:
        return fake.country()

def generate_string_province(**kwargs):
    """
    Generate a province/state name.
    Tries 'province()' first (for locales like en_CA), falls back to 'state()' (for locales like en_US, en_IN).
    """
    try:
        return fake.province()
    except AttributeError:
        # Many locales use 'state' instead of 'province' (e.g., en_US, en_IN)
        try:
            return fake.state()
        except AttributeError:
            raise GeneratorError(
                f"Locale '{fake.locale}' does not support province or state generation. "
                f"Available methods may vary by locale."
            )

def generate_string_postal_code(**kwargs):
    return fake.postcode()

def generate_string_city(**kwargs):
    return fake.city()

def generate_string_random(params, directive_str, **kwargs):
    length = _get_required_param(params, "length", directive_str)
    if not isinstance(length, int) or length <= 0:
        raise GeneratorError(f"Invalid 'length' for string:random: {length} in '{directive_str}'")
    return fake.pystr(min_chars=length, max_chars=length)

def generate_string_regex(params, directive_str, **kwargs):
    pattern = _get_required_param(params, "pattern", directive_str)
    try:
        return exrex.getone(pattern)
    except Exception as e:
        raise GeneratorError(f"Error generating string from regex pattern '{pattern}' in '{directive_str}': {e}")

def _load_static_data():
    try:
        from .static_data import STATIC_DATA_SETS
        return STATIC_DATA_SETS
    except ImportError as e:
        raise GeneratorError(f"Failed to import static data: {e}")


def generate_string_static_data(params, directive_str, **kwargs):
    """
    Generate a random value from a static data set.
    
    Usage:
      "string:static_data(data_set=vehicle_brands)" - Random vehicle brand
      "string:static_data(data_set=vehicle_colors)" - Random vehicle color
      "string:static_data(data_set=model_names,key=Toyota)" - Random model for Toyota brand
      "string:static_data(data_set=model_names,key=vehicle_brands)" - Random model for a random brand
    
    Args:
        params: Dictionary containing 'data_set' parameter and optional 'key' parameter
        directive_str: Original directive string for error messages
    
    Returns:
        Random value from the specified static data set
    """
    data_set_name = _get_required_param(params, "data_set", directive_str)
    key = _get_optional_param(params, "key", None)
    
    # Load static data
    static_data = _load_static_data()
    
    # Get the requested data set (case-insensitive lookup)
    data_set_name_lower = data_set_name.lower().replace(' ', '_')
    data_set = None
    
    for key_name in static_data.keys():
        if key_name.lower().replace(' ', '_') == data_set_name_lower:
            data_set = static_data[key_name]
            break
    
    if data_set is None:
        available_sets = ', '.join(static_data.keys())
        raise GeneratorError(
            f"Static data set '{data_set_name}' not found in '{directive_str}'. "
            f"Available data sets: {available_sets}"
        )
    
    # Handle dictionary-based data sets (like model_names)
    if isinstance(data_set, dict):
        if key is None:
            # If no key provided, randomly select a key and then a value from that key's list
            if len(data_set) == 0:
                raise GeneratorError(
                    f"Static data set '{data_set_name}' is empty dictionary in '{directive_str}'"
                )
            random_key = random.choice(list(data_set.keys()))
            values = data_set[random_key]
            if not isinstance(values, list) or len(values) == 0:
                raise GeneratorError(
                    f"Values for key '{random_key}' in '{data_set_name}' are empty or not a list in '{directive_str}'"
                )
            return random.choice(values)
        else:
            # Key provided - check if it's a reference to another data set
            key_lower = key.lower().replace(' ', '_')
            
            # Check if key is a reference to another static data set (e.g., "vehicle_brands")
            if key_lower in [k.lower().replace(' ', '_') for k in static_data.keys()]:
                # Get a random value from the referenced data set
                referenced_set = None
                for k in static_data.keys():
                    if k.lower().replace(' ', '_') == key_lower:
                        referenced_set = static_data[k]
                        break
                
                if isinstance(referenced_set, list):
                    lookup_key = random.choice(referenced_set)
                else:
                    raise GeneratorError(
                        f"Referenced data set '{key}' is not a list in '{directive_str}'"
                    )
            else:
                # Use key as-is (direct brand name)
                lookup_key = key
            
            # Look up the key in the dictionary
            if lookup_key not in data_set:
                available_keys = ', '.join(list(data_set.keys())[:10])  # Show first 10
                raise GeneratorError(
                    f"Key '{lookup_key}' not found in '{data_set_name}' in '{directive_str}'. "
                    f"Available keys (sample): {available_keys}"
                )
            
            values = data_set[lookup_key]
            if not isinstance(values, list) or len(values) == 0:
                raise GeneratorError(
                    f"Values for key '{lookup_key}' in '{data_set_name}' are empty or not a list in '{directive_str}'"
                )
            
            return random.choice(values)
    
    # Handle list-based data sets
    elif isinstance(data_set, list):
        if len(data_set) == 0:
            raise GeneratorError(
                f"Static data set '{data_set_name}' is empty in '{directive_str}'"
            )
        if key is not None:
            raise GeneratorError(
                f"Parameter 'key' is not supported for list-based data set '{data_set_name}' in '{directive_str}'"
            )
        return random.choice(data_set)


def generate_string_vehicle_brand_and_model(params, directive_str, **kwargs):
    """
    Generate a vehicle brand and model together, ensuring the model matches the brand.
    Uses thread-local storage to maintain brand state across field generations.
    
    Usage:
      "string:vehicle_brand_and_model" - Returns a random brand (stores it for model lookup)
      "string:vehicle_brand_and_model(return=model)" - Returns a model for the stored brand
      "string:vehicle_brand_and_model(return=both)" - Returns "Brand Model" format
      "string:vehicle_brand_and_model(return=model,key=brand)" - Uses the brand from the 'brand' field
    
    Args:
        params: Dictionary with optional 'return' parameter ('brand', 'model', or 'both')
               and optional 'key' parameter to reference another field name
        directive_str: Original directive string for error messages
    
    Returns:
        Brand, model, or "Brand Model" depending on return parameter
    """
    try:
        from .static_data import VEHICLE_BRANDS, MODEL_NAMES
    except ImportError as e:
        raise GeneratorError(f"Failed to import vehicle data: {e}")
    
    return_type = _get_optional_param(params, "return", "brand")
    key_field = _get_optional_param(params, "key", None)
    
    # Initialize thread-local storage if needed
    if not hasattr(_thread_local, 'vehicle_brand_cache'):
        _thread_local.vehicle_brand_cache = {}
    
    # If return_type is "brand", generate and store a brand
    if return_type == "brand" or return_type is None:
        brand = random.choice(VEHICLE_BRANDS)
        # Store in cache using the field name from base_dir or a default key
        cache_key = key_field if key_field else "default_brand"
        _thread_local.vehicle_brand_cache[cache_key] = brand
        return brand
    
    # For model generation, get the brand from cache or generate new one
    cache_key = key_field if key_field else "default_brand"
    
    if return_type == "model":
        # Try to get brand from cache
        if hasattr(_thread_local, 'vehicle_brand_cache') and cache_key in _thread_local.vehicle_brand_cache:
            brand = _thread_local.vehicle_brand_cache[cache_key]
        else:
            # If not in cache, generate a new brand
            brand = random.choice(VEHICLE_BRANDS)
            _thread_local.vehicle_brand_cache[cache_key] = brand
        
        # Get models for this brand
        if brand not in MODEL_NAMES:
            raise GeneratorError(
                f"Brand '{brand}' not found in MODEL_NAMES in '{directive_str}'"
            )
        
        models = MODEL_NAMES[brand]
        if not models or len(models) == 0:
            raise GeneratorError(
                f"No models found for brand '{brand}' in '{directive_str}'"
            )
        
        return random.choice(models)
    
    elif return_type == "both":
        brand = random.choice(VEHICLE_BRANDS)
        if brand not in MODEL_NAMES:
            raise GeneratorError(
                f"Brand '{brand}' not found in MODEL_NAMES in '{directive_str}'"
            )
        models = MODEL_NAMES[brand]
        if not models or len(models) == 0:
            raise GeneratorError(
                f"No models found for brand '{brand}' in '{directive_str}'"
            )
        model = random.choice(models)
        return f"{brand} {model}"
    
    else:
        raise GeneratorError(
            f"Invalid return type '{return_type}' in '{directive_str}'. Use 'brand', 'model', or 'both'"
        )

# --- Integer Generators ---
def generate_integer_range(params, directive_str, **kwargs):
    min_val = _get_required_param(params, "min", directive_str)
    max_val = _get_required_param(params, "max", directive_str)
    if not (isinstance(min_val, int) and isinstance(max_val, int)):
        raise GeneratorError(f"Parameters 'min' and 'max' must be integers for integer:range in '{directive_str}'")
    if min_val > max_val:
        raise GeneratorError(
            f"'min' ({min_val}) cannot be greater than 'max' ({max_val}) for integer:range in '{directive_str}'")
    return random.randint(min_val, max_val)

# --- Float Generators ---
def generate_float_range(params, directive_str, **kwargs):
    min_val = _get_required_param(params, "min", directive_str)
    max_val = _get_required_param(params, "max", directive_str)
    dp = _get_optional_param(params, "dp", 2)  # Default decimal places

    if not (isinstance(min_val, (int, float)) and isinstance(max_val, (int, float))):
        raise GeneratorError(f"Parameters 'min' and 'max' must be numbers for float:range in '{directive_str}'")
    if not isinstance(dp, int) or dp < 0:
        raise GeneratorError(f"Parameter 'dp' must be a non-negative integer for float:range in '{directive_str}'")
    if min_val > max_val:
        raise GeneratorError(
            f"'min' ({min_val}) cannot be greater than 'max' ({max_val}) for float:range in '{directive_str}'")

    val = random.uniform(min_val, max_val)
    return round(val, dp)

# --- Boolean Generators ---
def generate_boolean_random(**kwargs):
    return random.choice([True, False])

# --- Date Generators ---
def _parse_relative_date(date_str):
    """Parses relative date strings like '-30d', '+1y' into timedelta."""
    # This is a simplified parser. A more robust one might be needed.
    if isinstance(date_str, str):
        if date_str.endswith('d'):
            return timedelta(days=int(date_str[:-1]))
        elif date_str.endswith('y'):
            return timedelta(days=int(date_str[:-1]) * 365)  # Approximate for years
        elif date_str.endswith('m'):  # months, also approximate
            return timedelta(days=int(date_str[:-1]) * 30)
    raise ValueError(f"Invalid relative date string: {date_str}")

def generate_date_past(params, directive_str, **kwargs):
    years = _get_optional_param(params, "years", 1)
    date_format = _get_required_param(params, "format", directive_str)
    try:
        # Faker's past_date takes end_date as 'now' by default
        # and start_date relative to end_date.
        # So, if we want up to N years ago, it means start_date = "Ny"
        past_dt = fake.past_datetime(start_date=f"-{years}y", tzinfo=timezone.utc)
        return past_dt.strftime(date_format)
    except Exception as e:
        raise GeneratorError(f"Error generating past date for '{directive_str}': {e}")


def generate_date_future(params, directive_str, **kwargs):
    days = _get_optional_param(params, "days", 30)
    date_format = _get_required_param(params, "format", directive_str)
    try:
        # Faker's future_datetime takes start_date as 'now' by default
        # and end_date relative to start_date.
        future_dt = fake.future_datetime(end_date=f"+{days}d", tzinfo=timezone.utc)
        return future_dt.strftime(date_format)
    except Exception as e:
        raise GeneratorError(f"Error generating future date for '{directive_str}': {e}")


def generate_date_between(params, directive_str, **kwargs):
    start_date_str = _get_required_param(params, "start_date_str", directive_str)
    end_date_str = _get_required_param(params, "end_date_str", directive_str)
    date_format = _get_required_param(params, "format", directive_str)
    try:
        # Faker's date_time_between can take strings like "-30y", "now", "+1M"
        # It can also take datetime objects.
        dt_obj = fake.date_time_between(start_date=start_date_str, end_date=end_date_str, tzinfo=timezone.utc)
        return dt_obj.strftime(date_format)
    except Exception as e:
        raise GeneratorError(f"Error generating date between for '{directive_str}': {e}")


def generate_date_now(params, directive_str, **kwargs):
    date_format = _get_required_param(params, "format", directive_str)
    try:
        return datetime.now(timezone.utc).strftime(date_format)
    except Exception as e:
        raise GeneratorError(f"Error generating current date for '{directive_str}': {e}")

def generate_birth_date(params, directive_str, **kwargs):
    """
    Generate a birth date as a string.
    Returns date in ISO format (YYYY-MM-DD) by default, or uses provided format.
    """
    date_format = _get_optional_param(params, "format", "%Y-%m-%d")
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=70)
    return birth_date.strftime(date_format)

# --- Array Generators ---
def generate_primitive_array(params, directive_str, base_dir, **kwargs):
    from .engine import generate_single_record  # Local import to break circular dependency

    count = _get_required_param(params, "count", directive_str)
    element_generator_details = _get_required_param(params, "element_generator_details", directive_str)

    if not isinstance(count, int) or count < 0:
        raise GeneratorError(f"Array 'count' must be a non-negative integer in '{directive_str}'")

    arr = []
    for _ in range(count):
        arr.append(generate_single_record(element_generator_details, base_dir))
    return arr


def generate_object_array(params, directive_str, base_dir, **kwargs):
    from .engine import generate_single_record  # Local import to break circular dependency

    count = _get_required_param(params, "count", directive_str)
    parsed_sub_schema = _get_required_param(params, "parsed_sub_schema", directive_str)

    if not isinstance(count, int) or count < 0:
        raise GeneratorError(f"Array 'count' must be a non-negative integer in '{directive_str}'")

    arr = []
    sub_schema_file_path = os.path.join(base_dir, params["schema_file"])  # Reconstruct absolute path
    actual_sub_schema_base_dir = os.path.dirname(sub_schema_file_path)

    for _ in range(count):
        arr.append(generate_single_record(parsed_sub_schema, actual_sub_schema_base_dir))
    return arr


# --- Dispatcher for generators ---
GENERATOR_MAP = {
    ("string", "email"): generate_string_email,
    ("string", "name"): generate_string_name,
    ("string", "phone"): generate_string_phone,
    ("string", "firstname"): generate_string_firstname,
    ("string", "lastname"): generate_string_lastname,
    ("string", "uuid"): generate_string_uuid,
    ("string", "lorem"): generate_string_lorem,  # Expects params like type, count
    ("string", "word"): generate_string_word,
    ("string", "street_address"): generate_string_street_address,
    ("string", "city"): generate_string_city,
    ("string", "country"): generate_string_country,
    ("string", "random"): generate_string_random,  # Expects length
    ("string", "regex"): generate_string_regex,  # Expects pattern
    ("string", "sentence"): lambda params, **kwargs: generate_string_lorem({**params, "type": "sentence"}, **kwargs),
    ("string", "text"): lambda params, **kwargs: generate_string_lorem({**params, "type": "text"}, **kwargs),
    ("string", "province"): generate_string_province,
    ("string", "postal_code"): generate_string_postal_code,
    ("string", "vat_number"): generate_string_vat_number,

    # --- Vehicle Generators ---
    ("string", "static_data"): generate_string_static_data,  # Generic static data generator
    ("string", "vehicle_brand_and_model"): generate_string_vehicle_brand_and_model,  # Brand and matching model

    ("integer", "range"): generate_integer_range,  # Expects min, max
    ("integer", "random"): generate_integer_range,  # Alias

    ("float", "range"): generate_float_range,  # Expects min, max, dp
    ("float", "random"): generate_float_range,  # Alias

    ("boolean", "random"): generate_boolean_random,

    ("date", "past"): generate_date_past,  # Expects years, format
    ("date", "future"): generate_date_future,  # Expects days, format
    ("date", "between"): generate_date_between,  # Expects start_date_str, end_date_str, format
    ("date", "now"): generate_date_now,  # Expects format
    ("date", "birth_date"): generate_birth_date,  # Expects format

    ("array", "primitive_array"): generate_primitive_array,  # Expects count, element_type, element_generator_details
    ("array", "object_array"): generate_object_array,  # Expects count, parsed_sub_schema
}


def dispatch_generator(parsed_directive_node, base_dir):
    """
    Calls the appropriate generator function based on the parsed directive.
    `parsed_directive_node` is the dict produced by `_parse_directive_string`.
    `base_dir` is for resolving relative paths, mainly for array:object sub-schemas.
    """
    data_type = parsed_directive_node["data_type"]
    generator_name = parsed_directive_node["generator_name"]
    params = parsed_directive_node.get("params", {})
    original_directive = parsed_directive_node.get("original_directive", "unknown directive")

    key = (data_type, generator_name)
    if key not in GENERATOR_MAP:
        raise GeneratorError(
            f"No generator found for type '{data_type}' and name '{generator_name}' in directive '{original_directive}'")

    generator_func = GENERATOR_MAP[key]

    # Pass necessary context to the generator function
    # Some generators need `params`, some `directive_str` for error messages, some `base_dir`
    try:
        return generator_func(
            params=params,
            directive_str=original_directive,
            base_dir=base_dir
            # Some functions might not use all of these, which is fine with **kwargs or specific signatures.
        )
    except TypeError as te:
        if not params and generator_name not in ["lorem", "random", "regex", "range", "past", "future", "between",
                                                 "now", "primitive_array", "object_array"]:
            try:
                return generator_func()  # For simple generators like string:email, string:name
            except Exception as e_simple:
                raise GeneratorError(
                    f"Error calling generator for '{original_directive}': {e_simple} (after TypeError: {te})")
        raise GeneratorError(
            f"TypeError calling generator for '{original_directive}': {te}. Check function signature and parameters.")
    except GeneratorError:  # Re-raise GeneratorErrors
        raise
    except Exception as e:
        raise GeneratorError(f"Unexpected error in generator for '{original_directive}': {e}")

