"""
Script to import a comprehensive set of medications into the database
"""
from app import app, db
from models import Medication, Specialty
import json

def import_medications():
    """Import a comprehensive set of medications into the database"""
    with app.app_context():
        # First check if we already have medications beyond our test data
        if Medication.query.count() > 5:
            print(f"Database already has {Medication.query.count()} medications. Skipping import.")
            return

        # Make sure we have specialties
        specialties = {
            "Cardiology": "Branch of medicine that deals with disorders of the heart and cardiovascular system.",
            "Psychiatry": "Branch of medicine focused on the diagnosis, treatment and prevention of mental disorders.",
            "Neurology": "Branch of medicine dealing with disorders of the nervous system.",
            "Gastroenterology": "Branch of medicine focused on the digestive system and its disorders.",
            "Pulmonology": "Branch of medicine that deals with diseases involving the respiratory tract.",
            "Endocrinology": "Branch of medicine dealing with hormone-related diseases.",
            "Infectious Disease": "Branch of medicine dealing with the diagnosis and treatment of infections."
        }
        
        for name, description in specialties.items():
            if not Specialty.query.filter_by(name=name).first():
                specialty = Specialty(name=name, description=description)
                db.session.add(specialty)
        
        db.session.commit()
        
        # Get specialty objects for later use
        specialty_objects = {s.name: s for s in Specialty.query.all()}
        
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
                "name": "Atorvastatin",
                "class_name": "Statin",
                "description": "HMG-CoA reductase inhibitor that lowers cholesterol levels in the blood.",
                "dosing": "10-80 mg once daily",
                "side_effects": ["Muscle pain", "Liver enzyme elevation", "Headache", "Digestive problems"],
                "contraindications": ["Active liver disease", "Pregnancy", "Breastfeeding"],
                "uses": ["Hyperlipidemia", "Prevention of cardiovascular disease"],
                "specialties": ["Cardiology", "Endocrinology"]
            },
            
            # Psychiatry medications
            {
                "name": "Sertraline",
                "class_name": "SSRI",
                "description": "Selective serotonin reuptake inhibitor used to treat depression, anxiety, and other mental health conditions.",
                "dosing": "50-200 mg once daily",
                "side_effects": ["Nausea", "Insomnia", "Sexual dysfunction", "Diarrhea"],
                "contraindications": ["MAO inhibitor use within 14 days", "Pimozide use"],
                "uses": ["Depression", "Panic Disorder", "PTSD", "OCD", "Social Anxiety Disorder"],
                "specialties": ["Psychiatry"]
            },
            {
                "name": "Quetiapine",
                "class_name": "Atypical Antipsychotic",
                "description": "Atypical antipsychotic medication used to treat schizophrenia, bipolar disorder, and major depressive disorder.",
                "dosing": "150-800 mg daily in divided doses",
                "side_effects": ["Sedation", "Weight gain", "Dizziness", "Dry mouth"],
                "contraindications": ["Dementia-related psychosis", "QT prolongation"],
                "uses": ["Schizophrenia", "Bipolar Disorder", "Major Depressive Disorder"],
                "specialties": ["Psychiatry"]
            },
            
            # Neurology medications
            {
                "name": "Levetiracetam",
                "class_name": "Anticonvulsant",
                "description": "Anticonvulsant medication used to treat epilepsy and seizures.",
                "dosing": "500-3000 mg daily in divided doses",
                "side_effects": ["Somnolence", "Dizziness", "Irritability", "Headache"],
                "contraindications": ["Hypersensitivity to levetiracetam"],
                "uses": ["Partial onset seizures", "Myoclonic seizures", "Primary generalized tonic-clonic seizures"],
                "specialties": ["Neurology"]
            },
            {
                "name": "Sumatriptan",
                "class_name": "Triptan",
                "description": "Selective serotonin receptor agonist used to treat migraine headaches.",
                "dosing": "25-100 mg as needed for migraine",
                "side_effects": ["Chest tightness", "Dizziness", "Fatigue", "Tingling sensation"],
                "contraindications": ["Ischemic heart disease", "Uncontrolled hypertension", "Hemiplegic migraine"],
                "uses": ["Acute migraine treatment", "Cluster headaches"],
                "specialties": ["Neurology"]
            },
            
            # Gastroenterology medications
            {
                "name": "Omeprazole",
                "class_name": "Proton Pump Inhibitor",
                "description": "Proton pump inhibitor that decreases stomach acid production.",
                "dosing": "20-40 mg daily",
                "side_effects": ["Headache", "Abdominal pain", "Nausea", "Diarrhea"],
                "contraindications": ["Hypersensitivity to PPIs", "Rilpivirine use"],
                "uses": ["GERD", "Peptic ulcer disease", "H. pylori eradication", "Zollinger-Ellison syndrome"],
                "specialties": ["Gastroenterology"]
            },
            {
                "name": "Mesalamine",
                "class_name": "5-ASA",
                "description": "Anti-inflammatory medication used to treat inflammatory bowel disease.",
                "dosing": "2.4-4.8 g daily in divided doses",
                "side_effects": ["Headache", "Abdominal pain", "Nausea", "Diarrhea"],
                "contraindications": ["Hypersensitivity to salicylates", "Severe renal impairment"],
                "uses": ["Ulcerative colitis", "Crohn's disease"],
                "specialties": ["Gastroenterology"]
            },
            
            # Pulmonology medications
            {
                "name": "Albuterol",
                "class_name": "Short-acting Beta Agonist",
                "description": "Short-acting beta-2 agonist that relaxes bronchial smooth muscle.",
                "dosing": "2 puffs every 4-6 hours as needed",
                "side_effects": ["Tremor", "Tachycardia", "Nervousness", "Headache"],
                "contraindications": ["Hypersensitivity to albuterol"],
                "uses": ["Bronchospasm", "Exercise-induced bronchospasm", "Asthma", "COPD"],
                "specialties": ["Pulmonology"]
            },
            {
                "name": "Fluticasone",
                "class_name": "Inhaled Corticosteroid",
                "description": "Synthetic corticosteroid with anti-inflammatory properties used to treat asthma and allergic rhinitis.",
                "dosing": "88-880 mcg twice daily",
                "side_effects": ["Oral thrush", "Hoarseness", "Sore throat", "Cough"],
                "contraindications": ["Untreated fungal infections", "Status asthmaticus"],
                "uses": ["Asthma", "Allergic rhinitis", "COPD"],
                "specialties": ["Pulmonology", "Allergy/Immunology"]
            },
            
            # Endocrinology medications
            {
                "name": "Metformin",
                "class_name": "Biguanide",
                "description": "Oral diabetes medication that helps control blood sugar levels.",
                "dosing": "500-2000 mg daily in divided doses",
                "side_effects": ["Diarrhea", "Nausea", "Abdominal discomfort", "Vitamin B12 deficiency"],
                "contraindications": ["Renal dysfunction", "Metabolic acidosis", "Severe infection"],
                "uses": ["Type 2 diabetes", "Prediabetes", "PCOS"],
                "specialties": ["Endocrinology"]
            },
            {
                "name": "Levothyroxine",
                "class_name": "Thyroid Hormone",
                "description": "Synthetic thyroid hormone used to treat hypothyroidism.",
                "dosing": "25-200 mcg once daily",
                "side_effects": ["Palpitations", "Nervousness", "Insomnia", "Weight loss"],
                "contraindications": ["Thyrotoxicosis", "Acute myocardial infarction"],
                "uses": ["Hypothyroidism", "Thyroid cancer", "Myxedema coma"],
                "specialties": ["Endocrinology"]
            },
            
            # Infectious Disease medications
            {
                "name": "Amoxicillin",
                "class_name": "Penicillin Antibiotic",
                "description": "Broad-spectrum penicillin antibiotic used to treat bacterial infections.",
                "dosing": "250-500 mg three times daily",
                "side_effects": ["Diarrhea", "Nausea", "Rash", "Vomiting"],
                "contraindications": ["Penicillin allergy", "Infectious mononucleosis"],
                "uses": ["Respiratory tract infections", "Urinary tract infections", "Skin infections", "H. pylori eradication"],
                "specialties": ["Infectious Disease"]
            },
            {
                "name": "Ciprofloxacin",
                "class_name": "Fluoroquinolone Antibiotic",
                "description": "Broad-spectrum fluoroquinolone antibiotic that inhibits bacterial DNA gyrase.",
                "dosing": "250-750 mg twice daily",
                "side_effects": ["Tendon rupture", "QT prolongation", "Diarrhea", "Nausea"],
                "contraindications": ["History of tendon disorders", "QT prolongation", "Myasthenia gravis"],
                "uses": ["Urinary tract infections", "Respiratory infections", "Gastrointestinal infections", "Skin infections"],
                "specialties": ["Infectious Disease"]
            }
        ]
        
        # Add medications to database
        for med_data in medications_data:
            # Check if medication already exists
            if Medication.query.filter_by(name=med_data["name"]).first():
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
        
        # Commit all changes
        db.session.commit()
        print(f"Successfully imported {len(medications_data)} medications")
        print(f"Total medications in database: {Medication.query.count()}")

if __name__ == "__main__":
    import_medications()
