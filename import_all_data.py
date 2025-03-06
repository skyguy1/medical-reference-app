"""
Main script to import all medical data into the database
"""
from app import app, db
from models import Condition, Medication, Specialty, Reference, Guideline
from data_importer_psychiatry import PsychiatryDataImporter
from data_importer_rheumatology import RheumatologyDataImporter
from data_importer_nephrology import NephrologyDataImporter
from data_importer_infectious import InfectiousDataImporter
import db_cleanup

def count_database_entries():
    """Count and display the number of entries in the database"""
    with app.app_context():
        conditions_count = Condition.query.count()
        medications_count = Medication.query.count()
        specialties_count = Specialty.query.count()
        references_count = Reference.query.count()
        guidelines_count = Guideline.query.count()
        
        print(f"\nDatabase Status:")
        print(f"-------------------")
        print(f"Conditions: {conditions_count}")
        print(f"Medications: {medications_count}")
        print(f"Specialties: {specialties_count}")
        print(f"References: {references_count}")
        print(f"Guidelines: {guidelines_count}")
        print(f"-------------------\n")

def import_all_data():
    """
    Import all medical data into the database
    """
    with app.app_context():
        print("Starting data import process...")
        
        # First, check current database status
        count_database_entries()
        
        # Import data from each specialty
        print("\n=== Importing Psychiatry Data ===")
        psychiatry_importer = PsychiatryDataImporter()
        psychiatry_importer.import_data()
        
        print("\n=== Importing Rheumatology Data ===")
        rheumatology_importer = RheumatologyDataImporter()
        rheumatology_importer.import_data()
        
        print("\n=== Importing Nephrology Data ===")
        nephrology_importer = NephrologyDataImporter()
        nephrology_importer.import_data()
        
        print("\n=== Importing Infectious Diseases Data ===")
        infectious_importer = InfectiousDataImporter()
        infectious_importer.import_data()
        
        # Run database cleanup to fix any malformed JSON
        print("\n=== Running Database Cleanup ===")
        db_cleanup.fix_json_fields()
        
        # Check final database status
        print("\nImport complete! Final database status:")
        count_database_entries()
        
        print("\nThe medical database has been successfully expanded with comprehensive data.")
        print("You can now restart the Flask application to see the updated content.")

if __name__ == "__main__":
    import_all_data()
