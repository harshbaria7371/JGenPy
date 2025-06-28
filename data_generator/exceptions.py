# data_generator/exceptions.py
"""
Custom exceptions for the Test Data Generator tool.
"""

class DataGeneratorError(Exception):
    """Base class for exceptions in this module."""
    pass

class InvalidSchemaError(DataGeneratorError):
    """Raised when the input JSON schema is invalid or malformed."""
    pass

class DirectiveError(DataGeneratorError):
    """Raised for errors related to parsing or processing directives."""
    pass

class GeneratorError(DataGeneratorError):
    """Raised for errors occurring during data generation for a specific field."""
    pass

class FileHandlingError(DataGeneratorError):
    """Raised for errors related to file input/output."""
    pass
