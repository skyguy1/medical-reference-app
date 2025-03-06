"""
Script to check database statistics and contents
"""
from app import app, db
from models import Condition, Medication, Reference, Specialty, Guideline

def check_database_stats():
    """Print database statistics"""
    with app.app_context():
        # Get counts
        conditions_count = Condition.query.count()
        medications_count = Medication.query.count()
        specialties_count = Specialty.query.count()
        references_count = Reference.query.count()
        guidelines_count = Guideline.query.count() if hasattr(Guideline, 'query') else 0
        
        # Print statistics
        print("\n=== DATABASE STATISTICS ===")
        print(f"Conditions: {conditions_count}")
        print(f"Medications: {medications_count}")
        print(f"Specialties: {specialties_count}")
        print(f"References: {references_count}")
        print(f"Guidelines: {guidelines_count}")
        
        # Print specialties and their conditions
        print("\n=== SPECIALTIES AND CONDITIONS ===")
        specialties = Specialty.query.order_by(Specialty.name).all()
        for specialty in specialties:
            conditions = Condition.query.filter_by(specialty_id=specialty.id).all()
            print(f"{specialty.name}: {len(conditions)} conditions")
            for i, condition in enumerate(conditions[:5]):  # Show only first 5 to avoid overwhelming output
                print(f"  {i+1}. {condition.name}")
            if len(conditions) > 5:
                print(f"  ... and {len(conditions) - 5} more conditions")
        
        # Print conditions with most medications
        print("\n=== TOP CONDITIONS BY MEDICATION COUNT ===")
        conditions = Condition.query.all()
        conditions_with_meds = [(c, len(c.medications)) for c in conditions]
        conditions_with_meds.sort(key=lambda x: x[1], reverse=True)
        for i, (condition, med_count) in enumerate(conditions_with_meds[:10]):
            print(f"{i+1}. {condition.name}: {med_count} medications")
        
        # Print medications with most conditions
        print("\n=== TOP MEDICATIONS BY CONDITION COUNT ===")
        medications = Medication.query.all()
        meds_with_conditions = [(m, len(m.conditions)) for m in medications]
        meds_with_conditions.sort(key=lambda x: x[1], reverse=True)
        for i, (medication, cond_count) in enumerate(meds_with_conditions[:10]):
            print(f"{i+1}. {medication.name}: {cond_count} conditions")

if __name__ == "__main__":
    check_database_stats()
