"""
Script to import a batch of medications into the database
"""
from app import app, db
from models import Medication, Specialty
import json

def import_medications_batch1():
    """Import the first batch of medications into the database"""
    with app.app_context():
        print("Starting medication import - Batch 1...")
        
        # Make sure we have specialties
        specialties = {
            "Cardiology": "Branch of medicine that deals with disorders of the heart and cardiovascular system.",
            "Psychiatry": "Branch of medicine focused on the diagnosis, treatment and prevention of mental disorders.",
            "Neurology": "Branch of medicine dealing with disorders of the nervous system."
        }
        
        specialty_objects = {}
        for name, description in specialties.items():
            specialty = Specialty.query.filter_by(name=name).first()
            if not specialty:
                specialty = Specialty(name=name, description=description)
                db.session.add(specialty)
                db.session.commit()
            specialty_objects[name] = specialty
        
        # Define medications with their specialties
        medications_data = [
            # Cardiology medications
            {
                "name": "Metoprolol",
                "class_name": "Beta Blocker",
                "description": "Selective beta-1 blocker used to treat high blood pressure, chest pain, and heart failure.",
                "dosing": "25-200 mg daily in divided doses",
                "side_effects": ["Fatigue", "Dizziness", "Bradycardia", "Hypotension"],
                "contraindications": ["Severe bradycardia", "Heart block", "Cardiogenic shock"],
                "uses": ["Hypertension", "Angina", "Heart Failure", "Post-MI"],
                "specialties": ["Cardiology"]
            },
            {
                "name": "Amlodipine",
                "class_name": "Calcium Channel Blocker",
                "description": "Calcium channel blocker that dilates blood vessels and improves blood flow.",
                "dosing": "2.5-10 mg once daily",
                "side_effects": ["Peripheral edema", "Headache", "Flushing", "Dizziness"],
                "contraindications": ["Severe hypotension", "Heart block", "Severe aortic stenosis"],
                "uses": ["Hypertension", "Angina", "Coronary Artery Disease"],
                "specialties": ["Cardiology"]
            },
            {
                "name": "Warfarin",
                "class_name": "Anticoagulant",
                "description": "Vitamin K antagonist that prevents blood clotting by inhibiting vitamin K-dependent clotting factors.",
                "dosing": "2-10 mg once daily, adjusted based on INR",
                "side_effects": ["Bleeding", "Bruising", "Nausea", "Skin necrosis (rare)"],
                "contraindications": ["Active bleeding", "Severe liver disease", "Recent surgery"],
                "uses": ["Atrial fibrillation", "Deep vein thrombosis", "Pulmonary embolism", "Mechanical heart valves"],
                "specialties": ["Cardiology"]
            },
            {
                "name": "Clopidogrel",
                "class_name": "Antiplatelet",
                "description": "P2Y12 inhibitor that prevents platelet aggregation and reduces the risk of arterial thrombosis.",
                "dosing": "75 mg once daily",
                "side_effects": ["Bleeding", "Bruising", "Diarrhea", "Rash"],
                "contraindications": ["Active bleeding", "Severe liver disease"],
                "uses": ["Acute coronary syndrome", "Recent myocardial infarction", "Recent stroke", "Peripheral arterial disease"],
                "specialties": ["Cardiology"]
            },
            {
                "name": "Furosemide",
                "class_name": "Loop Diuretic",
                "description": "Loop diuretic that inhibits sodium and chloride reabsorption in the kidneys, increasing urine output.",
                "dosing": "20-80 mg once or twice daily",
                "side_effects": ["Dehydration", "Electrolyte imbalances", "Hypotension", "Ototoxicity"],
                "contraindications": ["Anuria", "Severe electrolyte depletion"],
                "uses": ["Heart failure", "Edema", "Hypertension", "Renal failure"],
                "specialties": ["Cardiology", "Nephrology"]
            }
        ]
        
        # Add medications to database
        for med_data in medications_data:
            # Check if medication already exists
            if Medication.query.filter_by(name=med_data["name"]).first():
                print(f"Medication already exists: {med_data['name']}")
                continue
                
            # Create new medication
            medication = Medication(
                name=med_data["name"],
                class_name=med_data["class_name"],
                description=med_data["description"],
                dosing=med_data["dosing"],
                side_effects=json.dumps(med_data["side_effects"]),
                contraindications=json.dumps(med_data["contraindications"]),
                uses=json.dumps(med_data["uses"])
            )
            
            db.session.add(medication)
            db.session.flush()  # Get ID without committing
            
            # Add specialty relationships
            for specialty_name in med_data["specialties"]:
                if specialty_name in specialty_objects:
                    medication.specialties.append(specialty_objects[specialty_name])
            
            print(f"Added medication: {med_data['name']}")
        
        # Commit all changes
        db.session.commit()
        print(f"Successfully imported batch 1 of medications")
        print(f"Total medications in database: {Medication.query.count()}")

if __name__ == "__main__":
    import_medications_batch1()
