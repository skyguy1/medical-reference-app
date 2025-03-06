"""
Simple script to check the database structure and contents
"""
from app import app, db
from models import Condition, Medication, Reference, Specialty

def check_database():
    """Check database structure and contents"""
    with app.app_context():
        print("Checking database...")
        
        # Check conditions
        conditions = Condition.query.all()
        print(f"\nFound {len(conditions)} conditions:")
        for i, condition in enumerate(conditions):
            print(f"{i+1}. {condition.name} (Specialty: {condition.specialty.name if condition.specialty else 'None'})")
            print(f"   References: {[ref.title for ref in condition.references] if condition.references else 'None'}")
        
        # Check medications
        medications = Medication.query.all()
        print(f"\nFound {len(medications)} medications:")
        for i, medication in enumerate(medications):
            print(f"{i+1}. {medication.name} ({medication.class_name})")
            print(f"   References: {[ref.title for ref in medication.references] if medication.references else 'None'}")
        
        # Check specialties
        specialties = Specialty.query.all()
        print(f"\nFound {len(specialties)} specialties:")
        for i, specialty in enumerate(specialties):
            print(f"{i+1}. {specialty.name}")
            conditions_count = len([c for c in conditions if c.specialty and c.specialty.id == specialty.id])
            print(f"   Conditions: {conditions_count}")
        
        # Check references
        references = Reference.query.all()
        print(f"\nFound {len(references)} references:")
        for i, reference in enumerate(references[:10]):  # Show only first 10 to avoid overwhelming output
            print(f"{i+1}. {reference.title}")
            print(f"   URL: {reference.url}")
        
        if len(references) > 10:
            print(f"   ... and {len(references) - 10} more references")

if __name__ == "__main__":
    check_database()
