"""
Test script for data importers' add_condition and add_medication methods
"""
from app import app, db
from models import Condition, Medication, Specialty
from data_importer_base import BaseDataImporter

def test_base_importer_methods():
    """Test the base data importer's add_condition and add_medication methods directly"""
    with app.app_context():
        print("\n===== Testing BaseDataImporter Methods =====")
        
        # Create a test importer
        importer = BaseDataImporter(
            specialty_name="Test Specialty",
            specialty_description="A test specialty for debugging"
        )
        
        # Test add_condition
        print("\nTesting add_condition method...")
        test_condition = importer.add_condition(
            name="Test Condition",
            description="A test condition for debugging",
            symptoms=["Symptom 1", "Symptom 2"],
            treatments=["Treatment 1", "Treatment 2"],
            references=[{"title": "Test Reference", "url": "http://example.com"}]
        )
        
        if test_condition:
            print(f"✓ Successfully added test condition: {test_condition.name}")
            print(f"  - Description: {test_condition.description[:30]}...")
            print(f"  - Symptoms: {test_condition.symptoms[:30]}...")
            print(f"  - Treatments: {test_condition.treatments[:30]}...")
            print(f"  - Specialty: {test_condition.specialty.name}")
        else:
            print("✗ Failed to add test condition")
        
        # Test add_medication
        print("\nTesting add_medication method...")
        test_medication = importer.add_medication(
            name="Test Medication",
            class_name="Test Class",
            uses=["Test Condition"],
            side_effects=["Side Effect 1", "Side Effect 2"],
            dosing="Test dosing information",
            contraindications=["Contraindication 1"]
        )
        
        if test_medication:
            print(f"✓ Successfully added test medication: {test_medication.name}")
            print(f"  - Class: {test_medication.class_name}")
            print(f"  - Uses: {test_medication.uses[:30]}...")
            print(f"  - Side Effects: {test_medication.side_effects[:30]}...")
            print(f"  - Dosing: {test_medication.dosing[:30]}...")
            print(f"  - Contraindications: {test_medication.contraindications[:30]}...")
        else:
            print("✗ Failed to add test medication")
        
        # Test linking medication to condition
        print("\nTesting link_medication_to_condition method...")
        link_result = importer.link_medication_to_condition("Test Medication", "Test Condition")
        if link_result:
            print("✓ Successfully linked medication to condition")
        else:
            print("✗ Failed to link medication to condition")
        
        # Commit the changes
        db.session.commit()
        print("✓ Changes committed to database")
        
        # Check database counts
        print("\nVerifying database counts:")
        condition_count = Condition.query.count()
        medication_count = Medication.query.count()
        specialty_count = Specialty.query.count()
        
        print(f"Conditions: {condition_count}")
        print(f"Medications: {medication_count}")
        print(f"Specialties: {specialty_count}")
        
        # Check if condition is linked to specialty
        test_specialty = Specialty.query.filter_by(name="Test Specialty").first()
        if test_specialty:
            condition_count = Condition.query.filter_by(specialty_id=test_specialty.id).count()
            print(f"Conditions for Test Specialty: {condition_count}")
        
        print("\n===== BaseDataImporter Methods Test Complete =====")

if __name__ == "__main__":
    # Disable history tracking for testing
    import models
    models.ENABLE_HISTORY_TRACKING = False
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Test the base importer methods
    test_base_importer_methods()
    
    # Re-enable history tracking
    models.ENABLE_HISTORY_TRACKING = True
    print("\nHistory tracking re-enabled")
