"""
Export module for the medical reference app

This module provides functions to export medical data in various formats.
"""
import json
import csv
import os
import io
import pandas as pd
import xml.dom.minidom as md
import xml.etree.ElementTree as ET
from datetime import datetime
from models import Condition, Medication, Specialty, Reference, Guideline
from flask import send_file

# Create export directory if it doesn't exist
EXPORT_DIR = 'exports'
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_to_json(data, filename=None):
    """
    Export data to JSON format
    
    Args:
        data: Data to export
        filename: Optional filename to save the export
        
    Returns:
        str or file: JSON string or file path if filename is provided
    """
    if not filename:
        return json.dumps(data, indent=2)
    
    filepath = os.path.join(EXPORT_DIR, f"{filename}.json")
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filepath

def export_to_csv(data, headers, filename=None):
    """
    Export data to CSV format
    
    Args:
        data: Data to export (list of dictionaries)
        headers: List of column headers
        filename: Optional filename to save the export
        
    Returns:
        str or file: CSV string or file path if filename is provided
    """
    if not filename:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
    
    filepath = os.path.join(EXPORT_DIR, f"{filename}.csv")
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    return filepath

def export_to_excel(data, filename):
    """
    Export data to Excel format
    
    Args:
        data: Dictionary of sheet names and data (list of dictionaries)
        filename: Filename to save the export
        
    Returns:
        file: File path
    """
    filepath = os.path.join(EXPORT_DIR, f"{filename}.xlsx")
    
    # Create a Pandas Excel writer
    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    
    # Write each dataframe to a different worksheet
    for sheet_name, sheet_data in data.items():
        df = pd.DataFrame(sheet_data)
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # Close the Pandas Excel writer
    writer.close()
    
    return filepath

def export_to_xml(data, root_element, item_element, filename=None):
    """
    Export data to XML format
    
    Args:
        data: List of dictionaries to export
        root_element: Name of the root element
        item_element: Name of the item element
        filename: Optional filename to save the export
        
    Returns:
        str or file: XML string or file path if filename is provided
    """
    root = ET.Element(root_element)
    
    for item in data:
        item_elem = ET.SubElement(root, item_element)
        for key, value in item.items():
            if value is not None:
                child = ET.SubElement(item_elem, key)
                child.text = str(value)
    
    # Pretty print XML
    xml_string = ET.tostring(root, encoding='utf-8')
    dom = md.parseString(xml_string)
    pretty_xml = dom.toprettyxml(indent="  ")
    
    if not filename:
        return pretty_xml
    
    filepath = os.path.join(EXPORT_DIR, f"{filename}.xml")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    return filepath

def export_conditions(format='json', filename=None):
    """
    Export all conditions
    
    Args:
        format: Export format ('json', 'csv', 'xml', 'excel')
        filename: Optional filename to save the export
        
    Returns:
        str or file: Exported data or file path
    """
    conditions = Condition.query.all()
    data = []
    
    for condition in conditions:
        try:
            symptoms = json.loads(condition.symptoms) if condition.symptoms else []
            treatments = json.loads(condition.treatments) if condition.treatments else []
        except (json.JSONDecodeError, TypeError):
            symptoms = []
            treatments = []
        
        condition_data = {
            'id': condition.id,
            'name': condition.name,
            'description': condition.description,
            'symptoms': ', '.join(symptoms) if format in ['csv', 'excel'] else symptoms,
            'treatments': ', '.join(treatments) if format in ['csv', 'excel'] else treatments,
            'created_at': condition.created_at.isoformat() if condition.created_at else None,
            'updated_at': condition.updated_at.isoformat() if condition.updated_at else None,
            'version': condition.version
        }
        
        # Add related medications
        medications = [med.name for med in condition.medications]
        condition_data['medications'] = ', '.join(medications) if format in ['csv', 'excel'] else medications
        
        data.append(condition_data)
    
    if format == 'json':
        return export_to_json(data, filename)
    elif format == 'csv':
        headers = ['id', 'name', 'description', 'symptoms', 'treatments', 'medications', 
                  'created_at', 'updated_at', 'version']
        return export_to_csv(data, headers, filename)
    elif format == 'xml':
        return export_to_xml(data, 'conditions', 'condition', filename)
    elif format == 'excel':
        return export_to_excel({'Conditions': data}, filename or 'conditions')
    else:
        raise ValueError(f"Unsupported format: {format}")

def export_medications(format='json', filename=None):
    """
    Export all medications
    
    Args:
        format: Export format ('json', 'csv', 'xml', 'excel')
        filename: Optional filename to save the export
        
    Returns:
        str or file: Exported data or file path
    """
    medications = Medication.query.all()
    data = []
    
    for medication in medications:
        try:
            uses = json.loads(medication.uses) if medication.uses else []
            side_effects = json.loads(medication.side_effects) if medication.side_effects else []
            contraindications = json.loads(medication.contraindications) if medication.contraindications else []
        except (json.JSONDecodeError, TypeError):
            uses = []
            side_effects = []
            contraindications = []
        
        medication_data = {
            'id': medication.id,
            'name': medication.name,
            'class_name': medication.class_name,
            'uses': ', '.join(uses) if format in ['csv', 'excel'] else uses,
            'side_effects': ', '.join(side_effects) if format in ['csv', 'excel'] else side_effects,
            'dosing': medication.dosing,
            'contraindications': ', '.join(contraindications) if format in ['csv', 'excel'] else contraindications,
            'created_at': medication.created_at.isoformat() if medication.created_at else None,
            'updated_at': medication.updated_at.isoformat() if medication.updated_at else None,
            'version': medication.version
        }
        
        # Add related conditions
        conditions = [cond.name for cond in medication.conditions]
        medication_data['conditions'] = ', '.join(conditions) if format in ['csv', 'excel'] else conditions
        
        data.append(medication_data)
    
    if format == 'json':
        return export_to_json(data, filename)
    elif format == 'csv':
        headers = ['id', 'name', 'class_name', 'uses', 'side_effects', 'dosing', 
                  'contraindications', 'conditions', 'created_at', 'updated_at', 'version']
        return export_to_csv(data, headers, filename)
    elif format == 'xml':
        return export_to_xml(data, 'medications', 'medication', filename)
    elif format == 'excel':
        return export_to_excel({'Medications': data}, filename or 'medications')
    else:
        raise ValueError(f"Unsupported format: {format}")

def export_specialties(format='json', filename=None):
    """
    Export all specialties
    
    Args:
        format: Export format ('json', 'csv', 'xml', 'excel')
        filename: Optional filename to save the export
        
    Returns:
        str or file: Exported data or file path
    """
    specialties = Specialty.query.all()
    data = []
    
    for specialty in specialties:
        specialty_data = {
            'id': specialty.id,
            'name': specialty.name,
            'description': specialty.description,
            'created_at': specialty.created_at.isoformat() if specialty.created_at else None,
            'updated_at': specialty.updated_at.isoformat() if specialty.updated_at else None
        }
        
        data.append(specialty_data)
    
    if format == 'json':
        return export_to_json(data, filename)
    elif format == 'csv':
        headers = ['id', 'name', 'description', 'created_at', 'updated_at']
        return export_to_csv(data, headers, filename)
    elif format == 'xml':
        return export_to_xml(data, 'specialties', 'specialty', filename)
    elif format == 'excel':
        return export_to_excel({'Specialties': data}, filename or 'specialties')
    else:
        raise ValueError(f"Unsupported format: {format}")

def export_references(format='json', filename=None):
    """
    Export all references
    
    Args:
        format: Export format ('json', 'csv', 'xml', 'excel')
        filename: Optional filename to save the export
        
    Returns:
        str or file: Exported data or file path
    """
    references = Reference.query.all()
    data = []
    
    for reference in references:
        reference_data = {
            'id': reference.id,
            'title': reference.title,
            'authors': reference.authors,
            'publication': reference.publication,
            'year': reference.year,
            'url': reference.url,
            'doi': reference.doi,
            'description': reference.description,
            'created_at': reference.created_at.isoformat() if reference.created_at else None,
            'updated_at': reference.updated_at.isoformat() if reference.updated_at else None
        }
        
        # Add related conditions and medications
        conditions = [cond.name for cond in reference.conditions]
        medications = [med.name for med in reference.medications]
        
        reference_data['conditions'] = ', '.join(conditions) if format in ['csv', 'excel'] else conditions
        reference_data['medications'] = ', '.join(medications) if format in ['csv', 'excel'] else medications
        
        data.append(reference_data)
    
    if format == 'json':
        return export_to_json(data, filename)
    elif format == 'csv':
        headers = ['id', 'title', 'authors', 'publication', 'year', 'url', 'doi', 
                  'description', 'conditions', 'medications', 'created_at', 'updated_at']
        return export_to_csv(data, headers, filename)
    elif format == 'xml':
        return export_to_xml(data, 'references', 'reference', filename)
    elif format == 'excel':
        return export_to_excel({'References': data}, filename or 'references')
    else:
        raise ValueError(f"Unsupported format: {format}")

def export_guidelines(format='json', filename=None):
    """
    Export all guidelines
    
    Args:
        format: Export format ('json', 'csv', 'xml', 'excel')
        filename: Optional filename to save the export
        
    Returns:
        str or file: Exported data or file path
    """
    guidelines = Guideline.query.all()
    data = []
    
    for guideline in guidelines:
        guideline_data = {
            'id': guideline.id,
            'title': guideline.title,
            'organization': guideline.organization,
            'publication_year': guideline.publication_year,
            'url': guideline.url,
            'summary': guideline.summary,
            'specialty': guideline.specialty.name if guideline.specialty else None,
            'created_at': guideline.created_at.isoformat() if guideline.created_at else None,
            'updated_at': guideline.updated_at.isoformat() if guideline.updated_at else None,
            'version': guideline.version
        }
        
        data.append(guideline_data)
    
    if format == 'json':
        return export_to_json(data, filename)
    elif format == 'csv':
        headers = ['id', 'title', 'organization', 'publication_year', 'url', 'summary', 
                  'specialty', 'created_at', 'updated_at', 'version']
        return export_to_csv(data, headers, filename)
    elif format == 'xml':
        return export_to_xml(data, 'guidelines', 'guideline', filename)
    elif format == 'excel':
        return export_to_excel({'Guidelines': data}, filename or 'guidelines')
    else:
        raise ValueError(f"Unsupported format: {format}")

def export_all(format='excel', filename=None):
    """
    Export all medical data
    
    Args:
        format: Export format ('json', 'excel')
        filename: Optional filename to save the export
        
    Returns:
        str or file: Exported data or file path
    """
    if format not in ['json', 'excel']:
        raise ValueError("Export all only supports 'json' and 'excel' formats")
    
    # Get all data
    conditions = Condition.query.all()
    medications = Medication.query.all()
    specialties = Specialty.query.all()
    references = Reference.query.all()
    guidelines = Guideline.query.all()
    
    # Process conditions
    condition_data = []
    for condition in conditions:
        try:
            symptoms = json.loads(condition.symptoms) if condition.symptoms else []
            treatments = json.loads(condition.treatments) if condition.treatments else []
        except (json.JSONDecodeError, TypeError):
            symptoms = []
            treatments = []
        
        condition_dict = {
            'id': condition.id,
            'name': condition.name,
            'description': condition.description,
            'symptoms': ', '.join(symptoms) if format == 'excel' else symptoms,
            'treatments': ', '.join(treatments) if format == 'excel' else treatments,
            'medications': ', '.join([med.name for med in condition.medications]) if format == 'excel' else [med.name for med in condition.medications],
            'created_at': condition.created_at.isoformat() if condition.created_at else None,
            'updated_at': condition.updated_at.isoformat() if condition.updated_at else None,
            'version': condition.version
        }
        condition_data.append(condition_dict)
    
    # Process medications
    medication_data = []
    for medication in medications:
        try:
            uses = json.loads(medication.uses) if medication.uses else []
            side_effects = json.loads(medication.side_effects) if medication.side_effects else []
            contraindications = json.loads(medication.contraindications) if medication.contraindications else []
        except (json.JSONDecodeError, TypeError):
            uses = []
            side_effects = []
            contraindications = []
        
        medication_dict = {
            'id': medication.id,
            'name': medication.name,
            'class_name': medication.class_name,
            'uses': ', '.join(uses) if format == 'excel' else uses,
            'side_effects': ', '.join(side_effects) if format == 'excel' else side_effects,
            'dosing': medication.dosing,
            'contraindications': ', '.join(contraindications) if format == 'excel' else contraindications,
            'conditions': ', '.join([cond.name for cond in medication.conditions]) if format == 'excel' else [cond.name for cond in medication.conditions],
            'created_at': medication.created_at.isoformat() if medication.created_at else None,
            'updated_at': medication.updated_at.isoformat() if medication.updated_at else None,
            'version': medication.version
        }
        medication_data.append(medication_dict)
    
    # Process specialties
    specialty_data = []
    for specialty in specialties:
        specialty_dict = {
            'id': specialty.id,
            'name': specialty.name,
            'description': specialty.description,
            'created_at': specialty.created_at.isoformat() if specialty.created_at else None,
            'updated_at': specialty.updated_at.isoformat() if specialty.updated_at else None
        }
        specialty_data.append(specialty_dict)
    
    # Process references
    reference_data = []
    for reference in references:
        reference_dict = {
            'id': reference.id,
            'title': reference.title,
            'authors': reference.authors,
            'publication': reference.publication,
            'year': reference.year,
            'url': reference.url,
            'doi': reference.doi,
            'description': reference.description,
            'conditions': ', '.join([cond.name for cond in reference.conditions]) if format == 'excel' else [cond.name for cond in reference.conditions],
            'medications': ', '.join([med.name for med in reference.medications]) if format == 'excel' else [med.name for med in reference.medications],
            'created_at': reference.created_at.isoformat() if reference.created_at else None,
            'updated_at': reference.updated_at.isoformat() if reference.updated_at else None
        }
        reference_data.append(reference_dict)
    
    # Process guidelines
    guideline_data = []
    for guideline in guidelines:
        guideline_dict = {
            'id': guideline.id,
            'title': guideline.title,
            'organization': guideline.organization,
            'publication_year': guideline.publication_year,
            'url': guideline.url,
            'summary': guideline.summary,
            'specialty': guideline.specialty.name if guideline.specialty else None,
            'created_at': guideline.created_at.isoformat() if guideline.created_at else None,
            'updated_at': guideline.updated_at.isoformat() if guideline.updated_at else None,
            'version': guideline.version
        }
        guideline_data.append(guideline_dict)
    
    # Combine all data
    all_data = {
        'conditions': condition_data,
        'medications': medication_data,
        'specialties': specialty_data,
        'references': reference_data,
        'guidelines': guideline_data
    }
    
    if format == 'json':
        return export_to_json(all_data, filename or 'medical_data')
    elif format == 'excel':
        return export_to_excel({
            'Conditions': condition_data,
            'Medications': medication_data,
            'Specialties': specialty_data,
            'References': reference_data,
            'Guidelines': guideline_data
        }, filename or 'medical_data')

def generate_export_filename(data_type):
    """
    Generate a filename for export based on data type and current timestamp
    
    Args:
        data_type: Type of data being exported
        
    Returns:
        str: Generated filename
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{data_type}_{timestamp}"
