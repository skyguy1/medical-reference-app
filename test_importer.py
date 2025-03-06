"""
Test script for data importers
"""
from app import app, db
from models import Condition, Medication, Specialty
from data_importer_psychiatry import PsychiatryDataImporter
from data_importer_infectious import InfectiousDataImporter
from data_importer_cardiology import CardiologyDataImporter
from data_importer_neurology import NeurologyDataImporter
from data_importer_rheumatology import RheumatologyDataImporter
from data_importer_respiratory import RespiratoryDataImporter
from data_importer_gi import GIDataImporter

def test_psychiatry_importer():
    """Test the psychiatry data importer"""
    with app.app_context():
        importer = PsychiatryDataImporter()
        print("Testing PsychiatryDataImporter...")
        
        # Test specialty creation
        specialty = importer.specialty
        print(f"Using specialty: {specialty.name}")
        
        # Test condition creation
        conditions = importer.import_conditions()
        print(f"Imported {len(conditions) if conditions else 0} conditions")
        
        # Test medication creation
        medications = importer.import_medications()
        print(f"Imported {len(medications) if medications else 0} medications")
        
        # Commit the changes
        db.session.commit()
        print("Changes committed to database")

def test_infectious_importer():
    """Test the infectious diseases data importer"""
    with app.app_context():
        importer = InfectiousDataImporter()
        print("Testing InfectiousDataImporter...")
        
        # Test specialty creation
        specialty = importer.specialty
        print(f"Using specialty: {specialty.name}")
        
        # Test condition creation
        conditions = importer.import_conditions()
        print(f"Imported {len(conditions) if conditions else 0} conditions")
        
        # Test medication creation
        medications = importer.import_medications()
        print(f"Imported {len(medications) if medications else 0} medications")
        
        # Commit the changes
        db.session.commit()
        print("Changes committed to database")

def test_cardiology_importer():
    """Test the cardiology data importer"""
    with app.app_context():
        importer = CardiologyDataImporter()
        print("Testing CardiologyDataImporter...")
        
        # Test specialty creation
        specialty = importer.specialty
        print(f"Using specialty: {specialty.name}")
        
        # Test condition creation
        conditions = importer.import_conditions()
        print(f"Imported {len(conditions) if conditions else 0} conditions")
        
        # Test medication creation
        medications = importer.import_medications()
        print(f"Imported {len(medications) if medications else 0} medications")
        
        # Commit the changes
        db.session.commit()
        print("Changes committed to database")

def test_neurology_importer():
    """Test the neurology data importer"""
    with app.app_context():
        importer = NeurologyDataImporter()
        print("Testing NeurologyDataImporter...")
        
        # Test specialty creation
        specialty = importer.specialty
        print(f"Using specialty: {specialty.name}")
        
        # Test condition creation
        conditions = importer.import_conditions()
        print(f"Imported {len(conditions) if conditions else 0} conditions")
        
        # Test medication creation
        medications = importer.import_medications()
        print(f"Imported {len(medications) if medications else 0} medications")
        
        # Commit the changes
        db.session.commit()
        print("Changes committed to database")

def test_rheumatology_importer():
    """Test the rheumatology data importer"""
    with app.app_context():
        importer = RheumatologyDataImporter()
        print("Testing RheumatologyDataImporter...")
        
        # Test specialty creation
        specialty = importer.specialty
        print(f"Using specialty: {specialty.name}")
        
        # Test condition creation
        conditions = importer.import_conditions()
        print(f"Imported {len(conditions) if conditions else 0} conditions")
        
        # Test medication creation
        medications = importer.import_medications()
        print(f"Imported {len(medications) if medications else 0} medications")
        
        # Commit the changes
        db.session.commit()
        print("Changes committed to database")

def test_respiratory_importer():
    """Test the respiratory data importer"""
    with app.app_context():
        importer = RespiratoryDataImporter()
        print("Testing RespiratoryDataImporter...")
        
        # Test specialty creation
        specialty = importer.specialty
        print(f"Using specialty: {specialty.name}")
        
        # Test condition creation
        conditions = importer.import_conditions()
        print(f"Imported {len(conditions) if conditions else 0} conditions")
        
        # Test medication creation
        medications = importer.import_medications()
        print(f"Imported {len(medications) if medications else 0} medications")
        
        # Commit the changes
        db.session.commit()
        print("Changes committed to database")

def test_gi_importer():
    """Test the gastroenterology data importer"""
    with app.app_context():
        importer = GIDataImporter()
        print("Testing GIDataImporter...")
        
        # Test specialty creation
        specialty = importer.specialty
        print(f"Using specialty: {specialty.name}")
        
        # Test condition creation
        conditions = importer.import_conditions()
        print(f"Imported {len(conditions) if conditions else 0} conditions")
        
        # Test medication creation
        medications = importer.import_medications()
        print(f"Imported {len(medications) if medications else 0} medications")
        
        # Commit the changes
        db.session.commit()
        print("Changes committed to database")

if __name__ == "__main__":
    print("Testing data importers individually...")
    
    # Disable history tracking for testing
    import models
    models.ENABLE_HISTORY_TRACKING = False
    
    # Test each importer
    test_psychiatry_importer()
    test_infectious_importer()
    test_cardiology_importer()
    test_neurology_importer()
    test_rheumatology_importer()
    test_respiratory_importer()
    test_gi_importer()
    
    # Re-enable history tracking
    models.ENABLE_HISTORY_TRACKING = True
    print("History tracking re-enabled...")
    
    # Print database statistics
    from db_stats import check_database_stats
    check_database_stats()
