"""
API endpoints for the medical reference app

This module provides RESTful API endpoints for accessing and searching medical data.
"""
from flask import Blueprint, request, jsonify
from models import db, Condition, Medication, Specialty, Reference, Guideline
from sqlalchemy import or_
import json

api = Blueprint('api', __name__)

@api.route('/api/search', methods=['GET'])
def search():
    """
    Search across all medical data
    
    Query parameters:
    - q: Search query
    - type: Type of data to search (condition, medication, specialty, reference, guideline, all)
    - specialty: Filter by specialty
    - limit: Maximum number of results to return (default: 20)
    - offset: Offset for pagination (default: 0)
    
    Returns:
        JSON response with search results
    """
    query = request.args.get('q', '')
    data_type = request.args.get('type', 'all')
    specialty = request.args.get('specialty', '')
    limit = int(request.args.get('limit', 20))
    offset = int(request.args.get('offset', 0))
    
    results = {
        'conditions': [],
        'medications': [],
        'specialties': [],
        'references': [],
        'guidelines': []
    }
    
    # Search conditions
    if data_type in ['condition', 'all']:
        conditions_query = Condition.query.filter(
            or_(
                Condition.name.ilike(f'%{query}%'),
                Condition.description.ilike(f'%{query}%')
            )
        )
        
        if specialty:
            conditions_query = conditions_query.join(Specialty).filter(Specialty.name == specialty)
            
        conditions = conditions_query.limit(limit).offset(offset).all()
        results['conditions'] = [
            {
                'id': c.id,
                'name': c.name,
                'description': c.description,
                'symptoms': c.symptoms,
                'treatments': c.treatments,
                'specialty': c.specialty.name if c.specialty else None
            }
            for c in conditions
        ]
    
    # Search medications
    if data_type in ['medication', 'all']:
        medications_query = Medication.query.filter(
            or_(
                Medication.name.ilike(f'%{query}%'),
                Medication.description.ilike(f'%{query}%'),
                Medication.class_name.ilike(f'%{query}%')
            )
        )
        
        if specialty:
            medications_query = medications_query.join(Specialty).filter(Specialty.name == specialty)
            
        medications = medications_query.limit(limit).offset(offset).all()
        results['medications'] = [
            {
                'id': m.id,
                'name': m.name,
                'class_name': m.class_name,
                'uses': m.uses,
                'side_effects': m.side_effects,
                'dosing': m.dosing,
                'contraindications': m.contraindications,
                'specialty': m.specialty.name if m.specialty else None
            }
            for m in medications
        ]
    
    # Search specialties
    if data_type in ['specialty', 'all']:
        specialties_query = Specialty.query.filter(
            or_(
                Specialty.name.ilike(f'%{query}%'),
                Specialty.description.ilike(f'%{query}%')
            )
        )
        
        specialties = specialties_query.limit(limit).offset(offset).all()
        results['specialties'] = [
            {
                'id': s.id,
                'name': s.name,
                'description': s.description
            }
            for s in specialties
        ]
    
    # Search references
    if data_type in ['reference', 'all']:
        references_query = Reference.query.filter(
            or_(
                Reference.title.ilike(f'%{query}%'),
                Reference.authors.ilike(f'%{query}%'),
                Reference.publication.ilike(f'%{query}%')
            )
        )
        
        references = references_query.limit(limit).offset(offset).all()
        results['references'] = [
            {
                'id': r.id,
                'title': r.title,
                'url': r.url,
                'authors': r.authors,
                'publication': r.publication,
                'year': r.year,
                'doi': r.doi
            }
            for r in references
        ]
    
    # Search guidelines
    if data_type in ['guideline', 'all']:
        guidelines_query = Guideline.query.filter(
            or_(
                Guideline.title.ilike(f'%{query}%'),
                Guideline.organization.ilike(f'%{query}%'),
                Guideline.summary.ilike(f'%{query}%')
            )
        )
        
        if specialty:
            guidelines_query = guidelines_query.join(Specialty).filter(Specialty.name == specialty)
            
        guidelines = guidelines_query.limit(limit).offset(offset).all()
        results['guidelines'] = [
            {
                'id': g.id,
                'title': g.title,
                'organization': g.organization,
                'publication_year': g.publication_year,
                'summary': g.summary,
                'url': g.url,
                'specialty': g.specialty.name if g.specialty else None
            }
            for g in guidelines
        ]
    
    # Count total results
    total_results = sum(len(results[key]) for key in results)
    
    return jsonify({
        'query': query,
        'type': data_type,
        'specialty': specialty,
        'limit': limit,
        'offset': offset,
        'total_results': total_results,
        'results': results
    })

@api.route('/api/conditions', methods=['GET'])
def get_conditions():
    """Get all conditions or filter by specialty"""
    specialty = request.args.get('specialty', '')
    
    if specialty:
        conditions = Condition.query.join(Specialty).filter(Specialty.name == specialty).all()
    else:
        conditions = Condition.query.all()
    
    return jsonify({
        'count': len(conditions),
        'conditions': [
            {
                'id': c.id,
                'name': c.name,
                'description': c.description,
                'symptoms': c.symptoms,
                'treatments': c.treatments,
                'specialty': c.specialty.name if c.specialty else None
            }
            for c in conditions
        ]
    })

@api.route('/api/conditions/<int:condition_id>', methods=['GET'])
def get_condition(condition_id):
    """Get a specific condition by ID"""
    condition = Condition.query.get_or_404(condition_id)
    
    return jsonify({
        'id': condition.id,
        'name': condition.name,
        'description': condition.description,
        'symptoms': condition.symptoms,
        'treatments': condition.treatments,
        'specialty': condition.specialty.name if condition.specialty else None,
        'references': [
            {
                'id': r.id,
                'title': r.title,
                'url': r.url
            }
            for r in condition.references
        ] if condition.references else []
    })

@api.route('/api/medications', methods=['GET'])
def get_medications():
    """Get all medications or filter by specialty"""
    specialty = request.args.get('specialty', '')
    
    if specialty:
        medications = Medication.query.join(Specialty).filter(Specialty.name == specialty).all()
    else:
        medications = Medication.query.all()
    
    return jsonify({
        'count': len(medications),
        'medications': [
            {
                'id': m.id,
                'name': m.name,
                'class_name': m.class_name,
                'uses': m.uses,
                'side_effects': m.side_effects,
                'dosing': m.dosing,
                'contraindications': m.contraindications,
                'specialty': m.specialty.name if m.specialty else None
            }
            for m in medications
        ]
    })

@api.route('/api/medications/<int:medication_id>', methods=['GET'])
def get_medication(medication_id):
    """Get a specific medication by ID"""
    medication = Medication.query.get_or_404(medication_id)
    
    return jsonify({
        'id': medication.id,
        'name': medication.name,
        'class_name': medication.class_name,
        'uses': medication.uses,
        'side_effects': medication.side_effects,
        'dosing': medication.dosing,
        'contraindications': medication.contraindications,
        'specialty': medication.specialty.name if medication.specialty else None
    })

@api.route('/api/specialties', methods=['GET'])
def get_specialties():
    """Get all specialties"""
    specialties = Specialty.query.all()
    
    return jsonify({
        'count': len(specialties),
        'specialties': [
            {
                'id': s.id,
                'name': s.name,
                'description': s.description,
                'condition_count': len(s.conditions),
                'medication_count': len(s.medications),
                'guideline_count': len(s.guidelines)
            }
            for s in specialties
        ]
    })

@api.route('/api/specialties/<int:specialty_id>', methods=['GET'])
def get_specialty(specialty_id):
    """Get a specific specialty by ID"""
    specialty = Specialty.query.get_or_404(specialty_id)
    
    return jsonify({
        'id': specialty.id,
        'name': specialty.name,
        'description': specialty.description,
        'conditions': [{'id': c.id, 'name': c.name} for c in specialty.conditions],
        'medications': [{'id': m.id, 'name': m.name} for m in specialty.medications],
        'guidelines': [{'id': g.id, 'title': g.title} for g in specialty.guidelines]
    })

@api.route('/api/references', methods=['GET'])
def get_references():
    """Get all references"""
    references = Reference.query.all()
    
    return jsonify({
        'count': len(references),
        'references': [
            {
                'id': r.id,
                'title': r.title,
                'url': r.url,
                'authors': r.authors,
                'publication': r.publication,
                'year': r.year,
                'doi': r.doi
            }
            for r in references
        ]
    })

@api.route('/api/guidelines', methods=['GET'])
def get_guidelines():
    """Get all guidelines or filter by specialty"""
    specialty = request.args.get('specialty', '')
    
    if specialty:
        guidelines = Guideline.query.join(Specialty).filter(Specialty.name == specialty).all()
    else:
        guidelines = Guideline.query.all()
    
    return jsonify({
        'count': len(guidelines),
        'guidelines': [
            {
                'id': g.id,
                'title': g.title,
                'organization': g.organization,
                'publication_year': g.publication_year,
                'summary': g.summary,
                'url': g.url,
                'specialty': g.specialty.name if g.specialty else None
            }
            for g in guidelines
        ]
    })

@api.route('/api/export', methods=['GET'])
def export_data():
    """
    Export medical data in JSON format
    
    Query parameters:
    - type: Type of data to export (condition, medication, specialty, reference, guideline, all)
    - specialty: Filter by specialty
    
    Returns:
        JSON data for export
    """
    data_type = request.args.get('type', 'all')
    specialty = request.args.get('specialty', '')
    
    export_data = {}
    
    # Export conditions
    if data_type in ['condition', 'all']:
        conditions_query = Condition.query
        
        if specialty:
            conditions_query = conditions_query.join(Specialty).filter(Specialty.name == specialty)
            
        conditions = conditions_query.all()
        export_data['conditions'] = [
            {
                'id': c.id,
                'name': c.name,
                'description': c.description,
                'symptoms': c.symptoms,
                'treatments': c.treatments,
                'specialty': c.specialty.name if c.specialty else None,
                'references': [{'id': r.id, 'title': r.title} for r in c.references] if c.references else []
            }
            for c in conditions
        ]
    
    # Export medications
    if data_type in ['medication', 'all']:
        medications_query = Medication.query
        
        if specialty:
            medications_query = medications_query.join(Specialty).filter(Specialty.name == specialty)
            
        medications = medications_query.all()
        export_data['medications'] = [
            {
                'id': m.id,
                'name': m.name,
                'class_name': m.class_name,
                'uses': m.uses,
                'side_effects': m.side_effects,
                'dosing': m.dosing,
                'contraindications': m.contraindications,
                'specialty': m.specialty.name if m.specialty else None
            }
            for m in medications
        ]
    
    # Export specialties
    if data_type in ['specialty', 'all']:
        specialties = Specialty.query.all()
        export_data['specialties'] = [
            {
                'id': s.id,
                'name': s.name,
                'description': s.description
            }
            for s in specialties
        ]
    
    # Export references
    if data_type in ['reference', 'all']:
        references = Reference.query.all()
        export_data['references'] = [
            {
                'id': r.id,
                'title': r.title,
                'url': r.url,
                'authors': r.authors,
                'publication': r.publication,
                'year': r.year,
                'doi': r.doi
            }
            for r in references
        ]
    
    # Export guidelines
    if data_type in ['guideline', 'all']:
        guidelines_query = Guideline.query
        
        if specialty:
            guidelines_query = guidelines_query.join(Specialty).filter(Specialty.name == specialty)
            
        guidelines = guidelines_query.all()
        export_data['guidelines'] = [
            {
                'id': g.id,
                'title': g.title,
                'organization': g.organization,
                'publication_year': g.publication_year,
                'summary': g.summary,
                'url': g.url,
                'specialty': g.specialty.name if g.specialty else None
            }
            for g in guidelines
        ]
    
    return jsonify(export_data)
