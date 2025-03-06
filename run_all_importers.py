"""
Script to run all available data importers to fully populate the database
"""
from app import app, db
from models import Medication, Condition, Specialty
import importlib
import sys

def run_all_importers():
    """Run all available data importers"""
    with app.app_context():
        # List of all importers to run
        importers = [
            'data_importer_psychiatry',
            'data_importer_cardiology',
            'data_importer_dermatology',
            'data_importer_endocrinology',
            'data_importer_gi',
            'data_importer_infectious',
            'data_importer_nephrology',
            'data_importer_neurology',
            'data_importer_respiratory',
            'data_importer_rheumatology'
        ]
        
        print(f"Starting to run all data importers...")
        print(f"Initial database stats:")
        print(f"- Medications: {Medication.query.count()}")
        print(f"- Conditions: {Condition.query.count()}")
        print(f"- Specialties: {Specialty.query.count()}")
        print("-" * 50)
        
        # Run each importer
        for importer_name in importers:
            try:
                print(f"Running {importer_name}...")
                module = importlib.import_module(importer_name)
                
                # Get the importer class name (usually the first part of the module name + "DataImporter")
                specialty = importer_name.split('_')[-1].capitalize()
                class_name = f"{specialty}DataImporter"
                
                # Check if the class exists in the module
                if hasattr(module, class_name):
                    importer_class = getattr(module, class_name)
                    importer = importer_class()
                    importer.import_data()
                    print(f"Successfully ran {importer_name}")
                else:
                    print(f"Could not find {class_name} in {importer_name}")
                    
            except ImportError:
                print(f"Could not import {importer_name}. Skipping.")
            except Exception as e:
                print(f"Error running {importer_name}: {str(e)}")
                
        print("-" * 50)
        print(f"Final database stats:")
        print(f"- Medications: {Medication.query.count()}")
        print(f"- Conditions: {Condition.query.count()}")
        print(f"- Specialties: {Specialty.query.count()}")

if __name__ == "__main__":
    run_all_importers()
