"""
Script to run all batch importers and generate medication relationships
"""
from app import app, db
from models import Medication, Condition, Specialty, MedicationRelationship
import importlib
import sys
import json

def run_batch_importers():
    """Run all batch importers and generate medication relationships"""
    with app.app_context():
        # List of batch importers to run
        importers = [
            'import_medications_batch1',
            'import_medications_batch2',
            'import_medications_batch3'
        ]
        
        print(f"Starting to run all batch importers...")
        print(f"Initial database stats:")
        print(f"- Medications: {Medication.query.count()}")
        print(f"- Conditions: {Condition.query.count()}")
        print(f"- Specialties: {Specialty.query.count()}")
        print(f"- Medication Relationships: {MedicationRelationship.query.count()}")
        print("-" * 50)
        
        # Run each batch importer
        for importer_name in importers:
            try:
                print(f"Running {importer_name}...")
                module = importlib.import_module(importer_name)
                
                # Get the main function from the module (should match the module name)
                func_name = importer_name
                
                # Check if the function exists in the module
                if hasattr(module, func_name):
                    import_func = getattr(module, func_name)
                    import_func()
                    print(f"Successfully ran {importer_name}")
                else:
                    print(f"Could not find {func_name} in {importer_name}")
                    
            except ImportError:
                print(f"Could not import {importer_name}. Skipping.")
            except Exception as e:
                print(f"Error running {importer_name}: {str(e)}")
        
        # Generate medication relationships
        print("-" * 50)
        print("Generating medication relationships...")
        generate_medication_relationships()
        
        print("-" * 50)
        print(f"Final database stats:")
        print(f"- Medications: {Medication.query.count()}")
        print(f"- Conditions: {Condition.query.count()}")
        print(f"- Specialties: {Specialty.query.count()}")
        print(f"- Medication Relationships: {MedicationRelationship.query.count()}")

def generate_medication_relationships():
    """Generate relationships between medications based on class and uses"""
    # Clear existing relationships
    MedicationRelationship.query.delete()
    db.session.commit()
    
    # Get all medications
    medications = Medication.query.all()
    print(f"Processing {len(medications)} medications for relationships")
    
    # Create a dictionary to store medications by class
    class_dict = {}
    uses_dict = {}
    
    # Group medications by class and uses
    for med in medications:
        # Add to class dictionary
        if med.class_name not in class_dict:
            class_dict[med.class_name] = []
        class_dict[med.class_name].append(med)
        
        # Add to uses dictionary
        try:
            uses = json.loads(med.uses)
            for use in uses:
                if use not in uses_dict:
                    uses_dict[use] = []
                uses_dict[use].append(med)
        except (json.JSONDecodeError, TypeError):
            print(f"Warning: Could not parse uses for {med.name}")
    
    # Create relationships based on same class
    relationships_created = 0
    for class_name, meds in class_dict.items():
        if len(meds) > 1:  # Only create relationships if there are at least 2 medications in the class
            for i in range(len(meds)):
                for j in range(i+1, len(meds)):
                    relationship = MedicationRelationship(
                        medication_id=meds[i].id,
                        related_medication_id=meds[j].id,
                        relationship_type="same_class"
                    )
                    db.session.add(relationship)
                    
                    # Create the reverse relationship
                    relationship = MedicationRelationship(
                        medication_id=meds[j].id,
                        related_medication_id=meds[i].id,
                        relationship_type="same_class"
                    )
                    db.session.add(relationship)
                    relationships_created += 2
    
    # Create relationships based on same uses
    for use, meds in uses_dict.items():
        if len(meds) > 1:  # Only create relationships if there are at least 2 medications for the use
            for i in range(len(meds)):
                for j in range(i+1, len(meds)):
                    # Check if they're not already related by class
                    if meds[i].class_name != meds[j].class_name:
                        relationship = MedicationRelationship(
                            medication_id=meds[i].id,
                            related_medication_id=meds[j].id,
                            relationship_type="same_use"
                        )
                        db.session.add(relationship)
                        
                        # Create the reverse relationship
                        relationship = MedicationRelationship(
                            medication_id=meds[j].id,
                            related_medication_id=meds[i].id,
                            relationship_type="same_use"
                        )
                        db.session.add(relationship)
                        relationships_created += 2
    
    db.session.commit()
    print(f"Created {relationships_created} medication relationships")

if __name__ == "__main__":
    run_batch_importers()
