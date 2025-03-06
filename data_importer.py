import json
import os
import sqlite3
from app import app, db
from models import Condition, Medication, Specialty

# This script will import data in batches to avoid memory issues
# Run this script multiple times to add more data to the database

# Batch 1: Cardiovascular conditions and medications
CARDIOVASCULAR_DATA = {
    "conditions": [
        {
            "name": "Hypertension",
            "description": "High blood pressure is a common condition in which the long-term force of the blood against your artery walls is high enough that it may eventually cause health problems, such as heart disease.",
            "symptoms": ["Headaches", "Shortness of breath", "Nosebleeds"],
            "treatments": ["Lifestyle changes", "Medication", "Regular monitoring"],
            "references": ["JNC 8 Guidelines", "American Heart Association, 2023"]
        },
        {
            "name": "Coronary Artery Disease",
            "description": "Coronary artery disease is a condition in which the major blood vessels that supply your heart become damaged or diseased, often due to cholesterol-containing deposits (plaques) or inflammation.",
            "symptoms": ["Chest pain (angina)", "Shortness of breath", "Pain in the neck, jaw, throat, upper abdomen or back", "Nausea", "Fatigue"],
            "treatments": ["Lifestyle changes", "Medications", "Procedures to restore blood flow", "Cardiac rehabilitation"],
            "references": ["American Heart Association, 2023", "American College of Cardiology, 2022"]
        },
        {
            "name": "Heart Failure",
            "description": "Heart failure, sometimes known as congestive heart failure, occurs when your heart muscle doesn't pump blood as well as it should. When this happens, blood often backs up and fluid can build up in the lungs, causing shortness of breath.",
            "symptoms": ["Shortness of breath", "Fatigue and weakness", "Swelling in legs, ankles and feet", "Rapid or irregular heartbeat", "Reduced ability to exercise"],
            "treatments": ["Medications", "Lifestyle changes", "Devices to help your heart beat and contract properly", "Heart transplant"],
            "references": ["American Heart Association Heart Failure Guidelines, 2023", "European Society of Cardiology, 2022"]
        },
        {
            "name": "Atrial Fibrillation",
            "description": "Atrial fibrillation is an irregular and often rapid heart rate that can increase your risk of strokes, heart failure and other heart-related complications.",
            "symptoms": ["Palpitations", "Weakness", "Reduced ability to exercise", "Fatigue", "Lightheadedness", "Dizziness", "Shortness of breath", "Chest pain"],
            "treatments": ["Medications to control heart rate", "Medications to prevent blood clots", "Electrical cardioversion", "Catheter ablation"],
            "references": ["American Heart Association AFib Guidelines, 2023", "European Society of Cardiology, 2022"]
        },
        {
            "name": "Peripheral Artery Disease",
            "description": "Peripheral artery disease (PAD) is a common circulatory problem in which narrowed arteries reduce blood flow to your limbs. When you develop PAD, your extremities — usually your legs — don't receive enough blood flow to keep up with demand.",
            "symptoms": ["Painful cramping in the hips, thighs or calves when walking", "Leg numbness or weakness", "Coldness in lower leg or foot", "Sores on toes, feet or legs that won't heal", "Hair loss or slower hair growth on legs"],
            "treatments": ["Lifestyle changes", "Medications", "Angioplasty", "Bypass surgery"],
            "references": ["American Heart Association PAD Guidelines, 2023", "European Society of Cardiology, 2022"]
        }
    ],
    "medications": [
        {
            "name": "Lisinopril",
            "class": "ACE inhibitor",
            "uses": ["Hypertension", "Heart failure", "Post-myocardial infarction"],
            "side_effects": ["Dry cough", "Dizziness", "Headache", "Elevated potassium levels"],
            "dosing": "10-40 mg once daily",
            "contraindications": ["Pregnancy", "History of angioedema", "Bilateral renal artery stenosis"]
        },
        {
            "name": "Metoprolol",
            "class": "Beta-blocker",
            "uses": ["Hypertension", "Angina", "Heart failure", "Post-myocardial infarction"],
            "side_effects": ["Fatigue", "Dizziness", "Bradycardia", "Bronchospasm"],
            "dosing": "25-200 mg daily in divided doses",
            "contraindications": ["Severe bradycardia", "Heart block", "Cardiogenic shock"]
        },
        {
            "name": "Amlodipine",
            "class": "Calcium channel blocker",
            "uses": ["Hypertension", "Angina", "Coronary artery disease"],
            "side_effects": ["Peripheral edema", "Headache", "Flushing", "Dizziness"],
            "dosing": "2.5-10 mg once daily",
            "contraindications": ["Severe hypotension", "Severe aortic stenosis"]
        },
        {
            "name": "Warfarin",
            "class": "Anticoagulant",
            "uses": ["Atrial fibrillation", "Deep vein thrombosis", "Pulmonary embolism", "Mechanical heart valves"],
            "side_effects": ["Bleeding", "Bruising", "Rare: skin necrosis"],
            "dosing": "Individualized based on INR (typically 2-10 mg daily)",
            "contraindications": ["Active bleeding", "Severe liver disease", "Pregnancy (relative)"]
        },
        {
            "name": "Atorvastatin",
            "class": "HMG-CoA reductase inhibitor (statin)",
            "uses": ["Hyperlipidemia", "Prevention of cardiovascular disease", "Coronary artery disease"],
            "side_effects": ["Muscle pain", "Liver enzyme elevation", "Headache", "Digestive problems"],
            "dosing": "10-80 mg once daily",
            "contraindications": ["Active liver disease", "Pregnancy", "Breastfeeding"]
        }
    ]
}

def import_cardiovascular_data():
    with app.app_context():
        # Check if specialty exists
        cardiology = Specialty.query.filter_by(name="Cardiology").first()
        if not cardiology:
            print("Error: Cardiology specialty not found. Run the main app first to initialize basic data.")
            return
        
        # Import conditions
        for condition_data in CARDIOVASCULAR_DATA['conditions']:
            # Check if condition already exists
            existing = Condition.query.filter_by(name=condition_data['name']).first()
            if existing:
                print(f"Condition {condition_data['name']} already exists, skipping.")
                continue
                
            condition = Condition(
                name=condition_data['name'],
                description=condition_data['description'],
                symptoms=json.dumps(condition_data['symptoms']),
                treatments=json.dumps(condition_data['treatments']),
                references=json.dumps(condition_data['references'])
            )
            condition.specialties.append(cardiology)
            db.session.add(condition)
            print(f"Added condition: {condition_data['name']}")
        
        # Import medications
        for medication_data in CARDIOVASCULAR_DATA['medications']:
            # Check if medication already exists
            existing = Medication.query.filter_by(name=medication_data['name']).first()
            if existing:
                print(f"Medication {medication_data['name']} already exists, skipping.")
                continue
                
            medication = Medication(
                name=medication_data['name'],
                class_name=medication_data['class'],
                uses=json.dumps(medication_data['uses']),
                side_effects=json.dumps(medication_data['side_effects']),
                dosing=medication_data['dosing'],
                contraindications=json.dumps(medication_data['contraindications'])
            )
            db.session.add(medication)
            print(f"Added medication: {medication_data['name']}")
            
            # Link medication to relevant conditions
            for use in medication_data['uses']:
                condition = Condition.query.filter(Condition.name.ilike(f"%{use}%")).first()
                if condition:
                    condition.medications.append(medication)
                    print(f"Linked {medication_data['name']} to {condition.name}")
        
        db.session.commit()
        print("Cardiovascular data import complete!")

if __name__ == "__main__":
    import_cardiovascular_data()
