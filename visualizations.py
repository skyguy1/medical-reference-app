"""
Visualization module for the medical reference app

This module provides functions to generate interactive visualizations for medical data.
"""
from models import db, Condition, Medication, Specialty, Reference, Guideline
from sqlalchemy import func
import json

def get_specialty_distribution():
    """
    Get data for specialty distribution visualization
    
    Returns:
        dict: Data for specialty distribution chart
    """
    # Query the database to get the count of conditions and medications per specialty
    specialty_data = db.session.query(
        Specialty.name,
        func.count(Condition.id).label('condition_count'),
        func.count(Medication.id).label('medication_count')
    ).outerjoin(Condition).outerjoin(Medication).group_by(Specialty.name).all()
    
    # Format data for visualization
    labels = []
    condition_counts = []
    medication_counts = []
    
    for specialty, condition_count, medication_count in specialty_data:
        labels.append(specialty)
        condition_counts.append(condition_count)
        medication_counts.append(medication_count)
    
    return {
        'labels': labels,
        'datasets': [
            {
                'label': 'Conditions',
                'data': condition_counts,
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Medications',
                'data': medication_counts,
                'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 1
            }
        ]
    }

def get_medication_class_distribution():
    """
    Get data for medication class distribution visualization
    
    Returns:
        dict: Data for medication class distribution chart
    """
    # Query the database to get the count of medications per class
    medication_class_data = db.session.query(
        Medication.class_name,
        func.count(Medication.id).label('count')
    ).group_by(Medication.class_name).all()
    
    # Format data for visualization
    labels = []
    counts = []
    background_colors = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(199, 199, 199, 0.2)',
        'rgba(83, 102, 255, 0.2)',
        'rgba(40, 159, 64, 0.2)',
        'rgba(210, 199, 199, 0.2)'
    ]
    border_colors = [color.replace('0.2', '1') for color in background_colors]
    
    for i, (class_name, count) in enumerate(medication_class_data):
        labels.append(class_name)
        counts.append(count)
    
    return {
        'labels': labels,
        'datasets': [{
            'label': 'Medications by Class',
            'data': counts,
            'backgroundColor': background_colors[:len(labels)],
            'borderColor': border_colors[:len(labels)],
            'borderWidth': 1
        }]
    }

def get_condition_network():
    """
    Get data for condition-medication network visualization
    
    Returns:
        dict: Data for network visualization
    """
    # Get all conditions with their medications
    conditions = Condition.query.all()
    
    nodes = []
    links = []
    
    # Add condition nodes
    for condition in conditions:
        nodes.append({
            'id': f'c{condition.id}',
            'name': condition.name,
            'type': 'condition',
            'group': 1
        })
        
        # Add medication nodes and links
        for medication in condition.medications:
            # Check if medication node already exists
            med_id = f'm{medication.id}'
            if not any(node['id'] == med_id for node in nodes):
                nodes.append({
                    'id': med_id,
                    'name': medication.name,
                    'type': 'medication',
                    'group': 2
                })
            
            # Add link between condition and medication
            links.append({
                'source': f'c{condition.id}',
                'target': f'm{medication.id}',
                'value': 1
            })
    
    return {
        'nodes': nodes,
        'links': links
    }

def get_reference_timeline():
    """
    Get data for reference timeline visualization
    
    Returns:
        dict: Data for timeline visualization
    """
    # Get all references with year
    references = Reference.query.filter(Reference.year.isnot(None)).order_by(Reference.year).all()
    
    # Group references by year
    years = {}
    for reference in references:
        year = reference.year
        if year not in years:
            years[year] = []
        
        years[year].append({
            'id': reference.id,
            'title': reference.title,
            'authors': reference.authors,
            'publication': reference.publication,
            'url': reference.url
        })
    
    # Format data for visualization
    timeline_data = []
    for year, refs in sorted(years.items()):
        timeline_data.append({
            'year': year,
            'count': len(refs),
            'references': refs
        })
    
    return timeline_data

def get_guideline_organization_distribution():
    """
    Get data for guideline organization distribution visualization
    
    Returns:
        dict: Data for guideline organization distribution chart
    """
    # Query the database to get the count of guidelines per organization
    organization_data = db.session.query(
        Guideline.organization,
        func.count(Guideline.id).label('count')
    ).group_by(Guideline.organization).all()
    
    # Format data for visualization
    labels = []
    counts = []
    
    for organization, count in organization_data:
        labels.append(organization)
        counts.append(count)
    
    return {
        'labels': labels,
        'datasets': [{
            'label': 'Guidelines by Organization',
            'data': counts,
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1
        }]
    }

def get_condition_symptom_heatmap():
    """
    Get data for condition-symptom heatmap visualization
    
    Returns:
        dict: Data for heatmap visualization
    """
    # Get all conditions with symptoms
    conditions = Condition.query.all()
    
    # Extract unique symptoms across all conditions
    all_symptoms = set()
    condition_symptoms = {}
    
    for condition in conditions:
        try:
            symptoms = json.loads(condition.symptoms) if condition.symptoms else []
            condition_symptoms[condition.name] = symptoms
            all_symptoms.update(symptoms)
        except (json.JSONDecodeError, TypeError):
            # Handle case where symptoms is not valid JSON
            pass
    
    # Convert to list for consistent ordering
    all_symptoms = sorted(list(all_symptoms))
    
    # Create heatmap data
    heatmap_data = []
    for condition_name, symptoms in condition_symptoms.items():
        for symptom in all_symptoms:
            value = 1 if symptom in symptoms else 0
            heatmap_data.append({
                'condition': condition_name,
                'symptom': symptom,
                'value': value
            })
    
    return {
        'symptoms': all_symptoms,
        'conditions': list(condition_symptoms.keys()),
        'data': heatmap_data
    }
