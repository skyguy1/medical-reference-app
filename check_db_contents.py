"""
Script to check database contents
"""
from app import app
from models import Condition, Medication, Specialty

def check_db_contents():
    """Check the contents of the database"""
    with app.app_context():
        # Count records
        condition_count = Condition.query.count()
        medication_count = Medication.query.count()
        specialty_count = Specialty.query.count()
        
        print(f"Database Contents:")
        print(f"Conditions: {condition_count}")
        print(f"Medications: {medication_count}")
        print(f"Specialties: {specialty_count}")
        
        # Sample conditions
        print("\nSample Conditions:")
        for condition in Condition.query.limit(5).all():
            print(f" - {condition.name} (Specialty: {condition.specialty.name if condition.specialty else 'None'})")
        
        # Sample medications
        print("\nSample Medications:")
        for medication in Medication.query.limit(5).all():
            print(f" - {medication.name} (Class: {medication.class_name})")
            print(f"   Description: {medication.description[:50]}...")
        
        # Check psychiatry data specifically
        print("\nPsychiatry Data:")
        psychiatry = Specialty.query.filter_by(name="Psychiatry").first()
        if psychiatry:
            psych_conditions = Condition.query.filter_by(specialty_id=psychiatry.id).count()
            psych_medications = Medication.query.filter_by(specialty_id=psychiatry.id).count()
            print(f"Psychiatry Conditions: {psych_conditions}")
            print(f"Psychiatry Medications: {psych_medications}")
            
            # List psychiatry medications
            print("\nPsychiatry Medications:")
            for med in Medication.query.filter_by(specialty_id=psychiatry.id).all():
                print(f" - {med.name}")
                print(f"   Description: {med.description[:50]}...")

if __name__ == "__main__":
    check_db_contents()
