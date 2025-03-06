"""
Validators for medical reference app data

This module provides validation functions for data before it's inserted into the database.
"""
import re
from datetime import datetime

def validate_condition(name, description, symptoms, treatments, references):
    """
    Validate condition data before insertion
    
    Args:
        name: Name of the condition
        description: Description of the condition
        symptoms: List of symptoms
        treatments: List of treatments
        references: List of references
        
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    # Validate name
    if not name or len(name) < 2:
        errors.append("Condition name must be at least 2 characters")
        print(f"Name validation failed: {name}")
    elif len(name) > 100:
        errors.append("Condition name must be less than 100 characters")
        print(f"Name validation failed (too long): {name}")
    
    # Validate description
    if not description or len(description) < 10:
        errors.append("Description must be at least 10 characters")
        print(f"Description validation failed: {description}")
    
    # Validate symptoms
    if not isinstance(symptoms, list):
        errors.append("Symptoms must be a list")
        print(f"Symptoms validation failed - not a list: {type(symptoms)}")
    elif not all(isinstance(s, str) for s in symptoms):
        errors.append("All symptoms must be strings")
        print(f"Symptoms validation failed - not all strings: {symptoms}")
    
    # Validate treatments
    if not isinstance(treatments, list):
        errors.append("Treatments must be a list")
        print(f"Treatments validation failed - not a list: {type(treatments)}")
    elif not all(isinstance(t, str) for t in treatments):
        errors.append("All treatments must be strings")
        print(f"Treatments validation failed - not all strings: {treatments}")
    
    # Validate references
    if not isinstance(references, list):
        errors.append("References must be a list")
        print(f"References validation failed - not a list: {type(references)}")
    
    return (len(errors) == 0, errors)

def validate_medication(name, class_name, uses, side_effects, dosing, contraindications):
    """
    Validate medication data before insertion
    
    Args:
        name: Name of the medication
        class_name: Class of the medication
        uses: Uses of the medication
        side_effects: Side effects of the medication
        dosing: Dosing information
        contraindications: Contraindications
        
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    # Validate name
    if not name or len(name) < 2:
        errors.append("Medication name must be at least 2 characters")
    elif len(name) > 100:
        errors.append("Medication name must be less than 100 characters")
    
    # Validate class_name
    if not class_name or len(class_name) < 2:
        errors.append("Class name must be at least 2 characters")
    elif len(class_name) > 100:
        errors.append("Class name must be less than 100 characters")
    
    # Validate uses
    if isinstance(uses, str):
        if len(uses) < 5:
            errors.append("Uses description must be at least 5 characters")
    elif isinstance(uses, list):
        if not all(isinstance(u, str) for u in uses):
            errors.append("All uses must be strings")
    else:
        errors.append("Uses must be a string or a list")
    
    # Validate side_effects
    if not isinstance(side_effects, list):
        errors.append("Side effects must be a list")
    elif not all(isinstance(s, str) for s in side_effects):
        errors.append("All side effects must be strings")
    
    # Validate dosing
    if not dosing or len(dosing) < 5:
        errors.append("Dosing information must be at least 5 characters")
    
    # Validate contraindications
    if not isinstance(contraindications, list):
        errors.append("Contraindications must be a list")
    elif not all(isinstance(c, str) for c in contraindications):
        errors.append("All contraindications must be strings")
    
    return (len(errors) == 0, errors)

def validate_reference(title, url=None, authors=None, publication=None, year=None, doi=None):
    """
    Validate reference data before insertion
    
    Args:
        title: Title of the reference
        url: URL of the reference
        authors: Authors of the reference
        publication: Publication name
        year: Publication year
        doi: Digital Object Identifier
        
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    # Validate title
    if not title or len(title) < 5:
        errors.append("Reference title must be at least 5 characters")
    elif len(title) > 200:
        errors.append("Reference title must be less than 200 characters")
    
    # Validate URL if provided
    if url:
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not url_pattern.match(url):
            errors.append("Invalid URL format")
    
    # Validate year if provided
    if year:
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if year_int < 1800 or year_int > current_year + 1:  # Allow for papers to be published next year
                errors.append(f"Year must be between 1800 and {current_year + 1}")
        except (ValueError, TypeError):
            errors.append("Year must be a valid integer")
    
    # Validate DOI if provided
    if doi:
        doi_pattern = re.compile(r'^10\.\d{4,9}/[-._;()/:A-Z0-9]+$', re.IGNORECASE)
        if not doi_pattern.match(doi):
            errors.append("Invalid DOI format (should be like 10.xxxx/xxxxx)")
    
    return (len(errors) == 0, errors)

def validate_guideline(title, organization, year, summary=None, url=None):
    """
    Validate guideline data before insertion
    
    Args:
        title: Title of the guideline
        organization: Organization that published the guideline
        year: Year the guideline was published
        summary: Summary of the guideline
        url: URL of the guideline
        
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    # Validate title
    if not title or len(title) < 5:
        errors.append("Guideline title must be at least 5 characters")
    elif len(title) > 200:
        errors.append("Guideline title must be less than 200 characters")
    
    # Validate organization
    if not organization or len(organization) < 2:
        errors.append("Organization name must be at least 2 characters")
    elif len(organization) > 200:
        errors.append("Organization name must be less than 200 characters")
    
    # Validate year
    try:
        year_int = int(year)
        current_year = datetime.now().year
        if year_int < 1800 or year_int > current_year + 1:  # Allow for guidelines to be published next year
            errors.append(f"Year must be between 1800 and {current_year + 1}")
    except (ValueError, TypeError):
        errors.append("Year must be a valid integer")
    
    # Validate URL if provided
    if url:
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not url_pattern.match(url):
            errors.append("Invalid URL format")
    
    return (len(errors) == 0, errors)
