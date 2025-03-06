"""
Script to import a second batch of medications into the database
"""
from app import app, db
from models import Medication, Specialty
import json

def import_medications_batch2():
    """Import the second batch of medications into the database"""
    with app.app_context():
        print("Starting medication import - Batch 2...")
        
        # Make sure we have specialties
        specialties = {
            "Psychiatry": "Branch of medicine focused on the diagnosis, treatment and prevention of mental disorders.",
            "Neurology": "Branch of medicine dealing with disorders of the nervous system.",
            "Endocrinology": "Branch of medicine dealing with hormone-related diseases.",
            "Infectious Disease": "Branch of medicine dealing with the diagnosis and treatment of infections."
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
            {
                "name": "Lithium",
                "class_name": "Mood Stabilizer",
                "description": "Mood stabilizer used primarily to treat bipolar disorder and prevent mood episodes.",
                "dosing": "600-1800 mg daily in divided doses, titrated to blood levels",
                "side_effects": ["Tremor", "Thirst", "Frequent urination", "Nausea", "Thyroid problems"],
                "contraindications": ["Severe renal impairment", "Dehydration", "Sodium depletion"],
                "uses": ["Bipolar Disorder", "Treatment-resistant depression", "Suicidality"],
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
        print(f"Successfully imported batch 2 of medications")
        print(f"Total medications in database: {Medication.query.count()}")

if __name__ == "__main__":
    import_medications_batch2()
