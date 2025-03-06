"""
Debug script for data importers
"""
import os
import sys
import traceback
from datetime import datetime

# Set up the Flask app context
from app import app, db
from models import Condition, Medication, Reference, Specialty, Guideline

# Disable history tracking
from models import ENABLE_HISTORY_TRACKING
import models
models.ENABLE_HISTORY_TRACKING = False

def test_single_importer(importer_class, specialty_name):
    """Test a single data importer with detailed error handling"""
    with app.app_context():
        print(f"\n===== Testing {specialty_name} Importer =====")
        
        try:
            # Initialize the importer
            print(f"Initializing {specialty_name} importer...")
            importer = importer_class()
            
            # Test specialty creation
            print(f"Checking specialty: {importer.specialty_name}")
            if importer.specialty:
                print(f"✓ Specialty found/created: {importer.specialty.name}")
            else:
                print(f"✗ Failed to create specialty")
            
            # Test condition import
            print(f"\nImporting {specialty_name} conditions...")
            try:
                conditions = importer.import_conditions()
                if conditions:
                    print(f"✓ Successfully imported {len(conditions)} conditions")
                else:
                    print(f"✗ No conditions imported")
            except Exception as e:
                print(f"✗ Error importing conditions: {str(e)}")
                traceback.print_exc()
            
            # Test medication import
            print(f"\nImporting {specialty_name} medications...")
            try:
                medications = importer.import_medications()
                if medications:
                    print(f"✓ Successfully imported {len(medications)} medications")
                else:
                    print(f"✗ No medications imported")
            except Exception as e:
                print(f"✗ Error importing medications: {str(e)}")
                traceback.print_exc()
            
            # Commit the changes
            print("\nCommitting changes to database...")
            db.session.commit()
            print("✓ Changes committed")
            
            # Check database counts
            print("\nVerifying database counts:")
            specialty = Specialty.query.filter_by(name=importer.specialty_name).first()
            if specialty:
                condition_count = Condition.query.filter_by(specialty_id=specialty.id).count()
                print(f"✓ {condition_count} conditions found for {specialty_name}")
                
                # Check if conditions are linked to the specialty
                if condition_count == 0:
                    print("✗ No conditions found for this specialty. Checking all conditions...")
                    all_conditions = Condition.query.all()
                    print(f"  Total conditions in database: {len(all_conditions)}")
                    for condition in all_conditions[:5]:  # Show first 5 for debugging
                        print(f"  - {condition.name} (Specialty ID: {condition.specialty_id})")
            else:
                print(f"✗ Specialty {specialty_name} not found in database")
            
            print(f"\n===== {specialty_name} Importer Test Complete =====")
            return True
            
        except Exception as e:
            print(f"✗ Unexpected error: {str(e)}")
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == "__main__":
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Test each importer individually
    from data_importer_psychiatry import PsychiatryDataImporter
    test_single_importer(PsychiatryDataImporter, "Psychiatry")
    
    from data_importer_infectious import InfectiousDataImporter
    test_single_importer(InfectiousDataImporter, "Infectious Diseases")
    
    from data_importer_cardiology import CardiologyDataImporter
    test_single_importer(CardiologyDataImporter, "Cardiology")
    
    from data_importer_neurology import NeurologyDataImporter
    test_single_importer(NeurologyDataImporter, "Neurology")
    
    from data_importer_rheumatology import RheumatologyDataImporter
    test_single_importer(RheumatologyDataImporter, "Rheumatology")
    
    from data_importer_respiratory import RespiratoryDataImporter
    test_single_importer(RespiratoryDataImporter, "Respiratory")
    
    from data_importer_gi import GIDataImporter
    test_single_importer(GIDataImporter, "Gastroenterology")
    
    # Re-enable history tracking
    models.ENABLE_HISTORY_TRACKING = True
    print("\nHistory tracking re-enabled")
    
    # Print final database statistics
    with app.app_context():
        print("\n===== DATABASE STATISTICS =====")
        print(f"Conditions: {Condition.query.count()}")
        print(f"Medications: {Medication.query.count()}")
        print(f"Specialties: {Specialty.query.count()}")
        print(f"References: {Reference.query.count()}")
        print(f"Guidelines: {Guideline.query.count()}")
        
        print("\n===== SPECIALTIES AND CONDITIONS =====")
        for specialty in Specialty.query.all():
            condition_count = Condition.query.filter_by(specialty_id=specialty.id).count()
            print(f"{specialty.name}: {condition_count} conditions")
