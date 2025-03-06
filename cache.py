"""
Caching module for the medical reference app

This module provides caching functionality to improve performance.
"""
from functools import wraps
import json
import os
import time
import hashlib

# Cache directory
CACHE_DIR = 'cache'
os.makedirs(CACHE_DIR, exist_ok=True)

# Default cache expiration time (in seconds)
DEFAULT_EXPIRATION = 3600  # 1 hour

def get_cache_key(func_name, *args, **kwargs):
    """
    Generate a unique cache key based on function name and arguments
    
    Args:
        func_name: Name of the function being cached
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        str: Cache key
    """
    # Create a string representation of the arguments
    arg_str = str(args) + str(sorted(kwargs.items()))
    
    # Create a hash of the arguments
    arg_hash = hashlib.md5(arg_str.encode()).hexdigest()
    
    # Combine function name and argument hash
    return f"{func_name}_{arg_hash}"

def cache_result(expiration=DEFAULT_EXPIRATION):
    """
    Decorator to cache function results
    
    Args:
        expiration: Cache expiration time in seconds
        
    Returns:
        function: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = get_cache_key(func.__name__, *args, **kwargs)
            cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
            
            # Check if cache file exists and is not expired
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                # Check if cache is expired
                if time.time() - cache_data['timestamp'] < expiration:
                    return cache_data['result']
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            
            # Save result to cache
            cache_data = {
                'timestamp': time.time(),
                'result': result
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
            
            return result
        return wrapper
    return decorator

def clear_cache():
    """Clear all cached data"""
    for file in os.listdir(CACHE_DIR):
        if file.endswith('.json'):
            os.remove(os.path.join(CACHE_DIR, file))

def clear_expired_cache(expiration=DEFAULT_EXPIRATION):
    """
    Clear expired cache files
    
    Args:
        expiration: Cache expiration time in seconds
    """
    current_time = time.time()
    
    for file in os.listdir(CACHE_DIR):
        if file.endswith('.json'):
            cache_file = os.path.join(CACHE_DIR, file)
            
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                # Check if cache is expired
                if current_time - cache_data['timestamp'] > expiration:
                    os.remove(cache_file)
            except (json.JSONDecodeError, KeyError, FileNotFoundError):
                # Remove invalid cache files
                os.remove(cache_file)
