"""
Database cleanup script to fix malformed JSON data in the database
"""
import json
import os
from app import app, db
from models import Condition, Medication, Specialty
from utils import safe_json_loads

def fix_json_fields():
    """
    Fix malformed JSON fields in the database
    
    This function:
    1. Checks all JSON fields in all models
    2. Attempts to parse them
    3. If parsing fails, sets them to a valid empty JSON string
    4. Commits the changes to the database
    """
    print("Starting database cleanup...")
    
    # Fix conditions
    print("Fixing conditions...")
    conditions = Condition.query.all()
    for condition in conditions:
        # Check symptoms
        try:
            json.loads(condition.symptoms) if condition.symptoms else []
        except (json.JSONDecodeError, TypeError):
            print(f"  Fixing symptoms for condition: {condition.name}")
            condition.symptoms = "[]"
            
        # Check treatments
        try:
            json.loads(condition.treatments) if condition.treatments else []
        except (json.JSONDecodeError, TypeError):
            print(f"  Fixing treatments for condition: {condition.name}")
            condition.treatments = "[]"
            
        # References are now handled as relationships, not JSON fields
    
    # Fix medications
    print("Fixing medications...")
    medications = Medication.query.all()
    for medication in medications:
        # Check uses
        try:
            json.loads(medication.uses) if medication.uses else []
        except (json.JSONDecodeError, TypeError):
            print(f"  Fixing uses for medication: {medication.name}")
            medication.uses = "[]"
            
        # Check side_effects
        try:
            json.loads(medication.side_effects) if medication.side_effects else []
        except (json.JSONDecodeError, TypeError):
            print(f"  Fixing side_effects for medication: {medication.name}")
            medication.side_effects = "[]"
            
        # Check contraindications
        try:
            json.loads(medication.contraindications) if medication.contraindications else []
        except (json.JSONDecodeError, TypeError):
            print(f"  Fixing contraindications for medication: {medication.name}")
            medication.contraindications = "[]"
    
    # Fix specialties
    print("Fixing specialties...")
    specialties = Specialty.query.all()
    for specialty in specialties:
        # Check topics
        try:
            json.loads(specialty.topics) if specialty.topics else []
        except (json.JSONDecodeError, TypeError):
            print(f"  Fixing topics for specialty: {specialty.name}")
            specialty.topics = "[]"
    
    # Commit changes
    print("Committing changes to database...")
    db.session.commit()
    
    print("Database cleanup complete!")

if __name__ == "__main__":
    with app.app_context():
        fix_json_fields()
