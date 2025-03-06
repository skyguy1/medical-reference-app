"""
Script to import a third batch of medications into the database
"""
from app import app, db
from models import Medication, Specialty
import json

def import_medications_batch3():
    """Import the third batch of medications into the database"""
    with app.app_context():
        print("Starting medication import - Batch 3...")
        
        # Make sure we have specialties
        specialties = {
            "Gastroenterology": "Branch of medicine focused on the digestive system and its disorders.",
            "Pulmonology": "Branch of medicine that deals with diseases involving the respiratory tract.",
            "Infectious Disease": "Branch of medicine dealing with the diagnosis and treatment of infections.",
            "Rheumatology": "Branch of medicine devoted to the diagnosis and treatment of rheumatic diseases."
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
            {
                "name": "Infliximab",
                "class_name": "TNF Inhibitor",
                "description": "Monoclonal antibody that blocks tumor necrosis factor alpha, reducing inflammation.",
                "dosing": "5 mg/kg IV at 0, 2, and 6 weeks, then every 8 weeks",
                "side_effects": ["Infusion reactions", "Increased risk of infections", "Headache", "Rash"],
                "contraindications": ["Active tuberculosis", "Moderate to severe heart failure", "Demyelinating disorders"],
                "uses": ["Crohn's disease", "Ulcerative colitis", "Rheumatoid arthritis", "Ankylosing spondylitis"],
                "specialties": ["Gastroenterology", "Rheumatology"]
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
            {
                "name": "Tiotropium",
                "class_name": "Long-acting Anticholinergic",
                "description": "Long-acting anticholinergic bronchodilator that helps open air passages in the lungs.",
                "dosing": "18 mcg once daily",
                "side_effects": ["Dry mouth", "Constipation", "Urinary retention", "Increased intraocular pressure"],
                "contraindications": ["Hypersensitivity to tiotropium", "Closed-angle glaucoma", "Prostatic hyperplasia"],
                "uses": ["COPD", "Asthma"],
                "specialties": ["Pulmonology"]
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
            },
            {
                "name": "Doxycycline",
                "class_name": "Tetracycline Antibiotic",
                "description": "Broad-spectrum tetracycline antibiotic that inhibits bacterial protein synthesis.",
                "dosing": "100 mg twice daily",
                "side_effects": ["Photosensitivity", "Esophageal irritation", "Nausea", "Diarrhea"],
                "contraindications": ["Pregnancy", "Children under 8 years", "Severe hepatic dysfunction"],
                "uses": ["Respiratory infections", "Skin infections", "Sexually transmitted infections", "Malaria prophylaxis"],
                "specialties": ["Infectious Disease", "Dermatology"]
            },
            
            # Rheumatology medications
            {
                "name": "Prednisone",
                "class_name": "Corticosteroid",
                "description": "Synthetic corticosteroid with potent anti-inflammatory and immunosuppressive properties.",
                "dosing": "5-60 mg daily, tapered as appropriate",
                "side_effects": ["Weight gain", "Mood changes", "Increased blood sugar", "Osteoporosis", "Increased infection risk"],
                "contraindications": ["Systemic fungal infections", "Live vaccines"],
                "uses": ["Rheumatoid arthritis", "Lupus", "Asthma", "Allergic reactions", "Many inflammatory conditions"],
                "specialties": ["Rheumatology", "Pulmonology", "Allergy/Immunology"]
            },
            {
                "name": "Methotrexate",
                "class_name": "DMARD",
                "description": "Disease-modifying antirheumatic drug that inhibits dihydrofolate reductase, reducing inflammation and immune system activity.",
                "dosing": "7.5-25 mg once weekly",
                "side_effects": ["Nausea", "Mouth sores", "Fatigue", "Liver enzyme elevation", "Bone marrow suppression"],
                "contraindications": ["Pregnancy", "Alcoholism", "Liver disease", "Immunodeficiency"],
                "uses": ["Rheumatoid arthritis", "Psoriatic arthritis", "Juvenile idiopathic arthritis", "Psoriasis"],
                "specialties": ["Rheumatology", "Dermatology"]
            },
            {
                "name": "Adalimumab",
                "class_name": "TNF Inhibitor",
                "description": "Monoclonal antibody that blocks tumor necrosis factor alpha, reducing inflammation in autoimmune diseases.",
                "dosing": "40 mg subcutaneously every other week",
                "side_effects": ["Injection site reactions", "Increased risk of infections", "Headache", "Rash"],
                "contraindications": ["Active tuberculosis", "Moderate to severe heart failure", "Demyelinating disorders"],
                "uses": ["Rheumatoid arthritis", "Psoriatic arthritis", "Ankylosing spondylitis", "Crohn's disease", "Ulcerative colitis"],
                "specialties": ["Rheumatology", "Gastroenterology", "Dermatology"]
            }
        ]
        
        # Add medications to database
        medications_added = 0
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
            
            medications_added += 1
            print(f"Added medication: {med_data['name']}")
        
        # Commit all changes
        db.session.commit()
        print(f"Successfully imported batch 3 of medications")
        print(f"Added {medications_added} new medications")
        print(f"Total medications in database: {Medication.query.count()}")

if __name__ == "__main__":
    import_medications_batch3()
