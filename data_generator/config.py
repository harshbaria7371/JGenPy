# data_generator/config.py
"""
Configuration management for JGenPy.
Reads settings from .config file and provides utilities for locale mapping.
"""
import os
from .exceptions import DataGeneratorError


CONFIG_FILE_NAME = ".config"
DEFAULT_LOCALE = "en_US"  # Default locale if no country is specified


# Mapping of country names to Faker locale codes
COUNTRY_TO_LOCALE = {
    "India": "en_IN",
    "United States": "en_US",
    "United Kingdom": "en_GB",
    "Canada": "en_CA",
    "Australia": "en_AU",
    "Germany": "de_DE",
    "France": "fr_FR",
    "Spain": "es_ES",
    "Italy": "it_IT",
    "Japan": "ja_JP",
    "China": "zh_CN",
    "Brazil": "pt_BR",
    "Mexico": "es_MX",
    "Russia": "ru_RU",
    "South Korea": "ko_KR",
    "Netherlands": "nl_NL",
    "Poland": "pl_PL",
    "Turkey": "tr_TR",
    "Sweden": "sv_SE",
    "Norway": "no_NO",
    "Denmark": "da_DK",
    "Finland": "fi_FI",
    "Greece": "el_GR",
    "Portugal": "pt_PT",
    "Czech Republic": "cs_CZ",
    "Hungary": "hu_HU",
    "Romania": "ro_RO",
    "Thailand": "th_TH",
    "Vietnam": "vi_VN",
    "Indonesia": "id_ID",
    "Malaysia": "ms_MY",
    "Singapore": "en_SG",
    "Philippines": "en_PH",
    "New Zealand": "en_NZ",
    "South Africa": "en_ZA",
    "Ireland": "en_IE",
    "Belgium": "nl_BE",
    "Switzerland": "de_CH",
    "Austria": "de_AT",
    "Argentina": "es_AR",
    "Chile": "es_CL",
    "Colombia": "es_CO",
    "Peru": "es_PE",
    "Venezuela": "es_VE",
    "Saudi Arabia": "ar_SA",
    "United Arab Emirates": "ar_AE",
    "Egypt": "ar_EG",
    "Israel": "he_IL",
    "Pakistan": "ur_PK",
    "Bangladesh": "bn_BD",
    "Sri Lanka": "si_LK",
    "Nepal": "ne_NP",
}


def get_config_file_path():
    """
    Returns the path to the .config file.
    Looks for it in the project root directory.
    """
    # Get the directory of this file (data_generator/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root
    project_root = os.path.dirname(current_dir)
    config_path = os.path.join(project_root, CONFIG_FILE_NAME)
    return config_path


def read_config():
    """
    Reads the .config file and returns a dictionary of key-value pairs.
    
    Returns:
        dict: Dictionary with config keys and values.
              Returns empty dict if file doesn't exist or is empty.
    """
    config = {}
    config_path = get_config_file_path()
    
    if not os.path.exists(config_path):
        return config
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse key=value format
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except Exception as e:
        raise DataGeneratorError(f"Error reading config file '{config_path}': {e}")
    
    return config


def get_country_from_config():
    """
    Reads the Country setting from .config file.
    
    Returns:
        str: Country name if found, None otherwise.
    """
    config = read_config()
    return config.get('Country')


def get_locale_for_country(country_name):
    """
    Maps a country name to a Faker locale code.
    
    Args:
        country_name: Name of the country (e.g., "India", "United States")
    
    Returns:
        str: Faker locale code (e.g., "en_IN", "en_US")
              Returns DEFAULT_LOCALE if country not found in mapping.
    """
    if not country_name:
        return DEFAULT_LOCALE
    
    # Case-insensitive lookup
    country_name_lower = country_name.strip().lower()
    for country, locale in COUNTRY_TO_LOCALE.items():
        if country.lower() == country_name_lower:
            return locale
    
    # If country not found, return default locale
    return DEFAULT_LOCALE


def get_configured_locale():
    """
    Gets the locale to use based on the Country setting in .config file.
    
    Returns:
        str: Faker locale code to use for data generation.
    """
    country = get_country_from_config()
    locale = get_locale_for_country(country)
    return locale

