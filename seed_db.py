"""
Standalone script to seed the database with data from all importers
"""
import os
import sys
from datetime import datetime

# Set up the Flask app context
from app import app, db
from models import Condition, Medication, Reference, Specialty, Guideline

# Disable history tracking
from models import ENABLE_HISTORY_TRACKING
import models
models.ENABLE_HISTORY_TRACKING = False

def seed_database():
    """Seed the database with data from all importers"""
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if database is already seeded
        if Condition.query.count() > 0:
            print("Database already seeded. Skipping...")
            return
        
        print("Seeding database with medical data...")
        
        try:
            # Import data from all importers
            importers = []
            
            # Cardiology
            print("Importing Cardiology data...")
            from data_importer_cardiology import CardiologyDataImporter
            importers.append(("Cardiology", CardiologyDataImporter()))
            
            # Psychiatry
            print("Importing Psychiatry data...")
            from data_importer_psychiatry import PsychiatryDataImporter
            importers.append(("Psychiatry", PsychiatryDataImporter()))
            
            # Infectious Diseases
            print("Importing Infectious Diseases data...")
            from data_importer_infectious import InfectiousDataImporter
            importers.append(("Infectious Diseases", InfectiousDataImporter()))
            
            # Rheumatology
            print("Importing Rheumatology data...")
            from data_importer_rheumatology import RheumatologyDataImporter
            importers.append(("Rheumatology", RheumatologyDataImporter()))
            
            # Neurology
            print("Importing Neurology data...")
            from data_importer_neurology import NeurologyDataImporter
            importers.append(("Neurology", NeurologyDataImporter()))
            
            # Respiratory
            print("Importing Respiratory data...")
            from data_importer_respiratory import RespiratoryDataImporter
            importers.append(("Respiratory", RespiratoryDataImporter()))
            
            # Gastroenterology
            print("Importing Gastroenterology data...")
            from data_importer_gi import GIDataImporter
            importers.append(("Gastroenterology", GIDataImporter()))
            
            # Dermatology
            print("Importing Dermatology data...")
            from data_importer_dermatology import DermatologyDataImporter
            importers.append(("Dermatology", DermatologyDataImporter()))
            
            # Endocrinology
            print("Importing Endocrinology data...")
            from data_importer_endocrinology import EndocrinologyDataImporter
            importers.append(("Endocrinology", EndocrinologyDataImporter()))
            
            # Nephrology
            print("Importing Nephrology data...")
            from data_importer_nephrology import NephrologyDataImporter
            importers.append(("Nephrology", NephrologyDataImporter()))
            
            # Import data from each importer
            for specialty_name, importer in importers:
                print(f"Running import for {specialty_name}...")
                try:
                    importer.import_data()
                    db.session.commit()
                    print(f"Successfully imported {specialty_name} data")
                except Exception as e:
                    db.session.rollback()
                    print(f"Error importing {specialty_name} data: {str(e)}")
                    # Log the error
                    with open('error_log.txt', 'a') as f:
                        f.write(f"{datetime.now()}: Error importing {specialty_name} data: {str(e)}\n")
            
            # Print database statistics
            print("\nDatabase seeding completed. Statistics:")
            print(f"Conditions: {Condition.query.count()}")
            print(f"Medications: {Medication.query.count()}")
            print(f"Specialties: {Specialty.query.count()}")
            print(f"References: {Reference.query.count()}")
            print(f"Guidelines: {Guideline.query.count() if hasattr(Guideline, 'query') else 0}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {str(e)}")
            # Log the error
            with open('error_log.txt', 'a') as f:
                f.write(f"{datetime.now()}: Error seeding database: {str(e)}\n")
        finally:
            # Re-enable history tracking
            models.ENABLE_HISTORY_TRACKING = True
            print("History tracking re-enabled")

if __name__ == "__main__":
    # Delete the database file if it exists and --reset flag is provided
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        db_path = "instance/medical_reference.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Deleted existing database file: {db_path}")
        else:
            print("No existing database file to delete")
    
    # Seed the database
    seed_database()
