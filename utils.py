"""
Utility functions for the medical reference application
"""
import json

def safe_json_loads(json_str, default=None):
    """
    Safely load JSON string with error handling
    
    Args:
        json_str: JSON string to parse
        default: Default value to return if parsing fails (default: None)
        
    Returns:
        Parsed JSON object or default value if parsing fails
    """
    if default is None:
        default = []
        
    if not json_str:
        return default
        
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError, ValueError):
        return default
