"""
Simple script to import basic data into the database
"""
from app import app, db
from models import Condition, Medication, Specialty
import json

def import_basic_data():
    """Import basic data into the database"""
    with app.app_context():
        # Create a specialty if none exists
        if Specialty.query.count() == 0:
            cardiology = Specialty(
                name="Cardiology",
                description="Branch of medicine that deals with disorders of the heart and cardiovascular system."
            )
            db.session.add(cardiology)
            
            psychiatry = Specialty(
                name="Psychiatry",
                description="Branch of medicine focused on the diagnosis, treatment and prevention of mental, emotional and behavioral disorders."
            )
            db.session.add(psychiatry)
            db.session.commit()
            print("Added specialties")
        
        # Create a condition if none exists
        if Condition.query.count() == 0:
            hypertension = Condition(
                name="Hypertension",
                description="High blood pressure is a common condition in which the long-term force of the blood against your artery walls is high enough that it may eventually cause health problems.",
                symptoms=["Headaches", "Shortness of breath", "Nosebleeds"],
                treatments=["Lifestyle changes", "Medication", "Regular monitoring"],
                specialty_id=1  # Cardiology
            )
            db.session.add(hypertension)
            
            depression = Condition(
                name="Major Depressive Disorder",
                description="A mood disorder characterized by persistent feelings of sadness and loss of interest.",
                symptoms=["Persistent sad mood", "Loss of interest", "Fatigue"],
                treatments=["Medication", "Psychotherapy", "Lifestyle changes"],
                specialty_id=2  # Psychiatry
            )
            db.session.add(depression)
            db.session.commit()
            print("Added conditions")
        
        # Create medications if none exist
        if Medication.query.count() == 0:
            lisinopril = Medication(
                name="Lisinopril",
                class_name="ACE Inhibitor",
                description="Used to treat high blood pressure and heart failure.",
                dosing="10-40 mg daily",
                side_effects=json.dumps(["Dry cough", "Dizziness", "Headache"]),
                contraindications=json.dumps(["Pregnancy", "History of angioedema"]),
                uses=json.dumps(["Hypertension", "Heart Failure", "Post-MI"])
            )
            db.session.add(lisinopril)
            
            fluoxetine = Medication(
                name="Fluoxetine",
                class_name="SSRI",
                description="Selective serotonin reuptake inhibitor used to treat depression and anxiety disorders.",
                dosing="20-80 mg daily",
                side_effects=json.dumps(["Nausea", "Insomnia", "Headache"]),
                contraindications=json.dumps(["MAO inhibitor use within 14 days"]),
                uses=json.dumps(["Depression", "OCD", "Panic Disorder"])
            )
            db.session.add(fluoxetine)
            db.session.commit()
            print("Added medications")
            
            # Add specialty relationships
            cardiology = Specialty.query.filter_by(name="Cardiology").first()
            psychiatry = Specialty.query.filter_by(name="Psychiatry").first()
            
            lisinopril = Medication.query.filter_by(name="Lisinopril").first()
            fluoxetine = Medication.query.filter_by(name="Fluoxetine").first()
            
            if cardiology and lisinopril:
                lisinopril.specialties.append(cardiology)
            
            if psychiatry and fluoxetine:
                fluoxetine.specialties.append(psychiatry)
                
            db.session.commit()
            print("Added medication-specialty relationships")

if __name__ == "__main__":
    import_basic_data()
    print("Basic data import complete")
