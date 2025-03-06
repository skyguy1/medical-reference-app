"""
Data importer for endocrinology conditions and medications
"""
import json
from models import db, Condition, Medication, Specialty
from data_importer_base import BaseDataImporter

# Endocrinology conditions and medications data
ENDOCRINOLOGY_DATA = {
    "conditions": [
        {
            "name": "Type 1 Diabetes Mellitus",
            "description": "Type 1 diabetes is a chronic condition in which the pancreas produces little or no insulin, a hormone needed to allow sugar (glucose) to enter cells to produce energy.",
            "symptoms": ["Increased thirst", "Frequent urination", "Extreme hunger", "Unintended weight loss", "Irritability and mood changes", "Fatigue and weakness", "Blurred vision"],
            "treatments": ["Insulin therapy", "Carbohydrate counting", "Frequent blood sugar monitoring", "Healthy eating", "Regular physical activity"],
            "references": ["American Diabetes Association Standards of Care, 2023", "International Society for Pediatric and Adolescent Diabetes, 2022"]
        },
        {
            "name": "Type 2 Diabetes Mellitus",
            "description": "Type 2 diabetes is a chronic condition that affects the way your body metabolizes sugar (glucose), your body's important source of fuel. With type 2 diabetes, your body either resists the effects of insulin or doesn't produce enough insulin to maintain normal glucose levels.",
            "symptoms": ["Increased thirst", "Frequent urination", "Increased hunger", "Unintended weight loss", "Fatigue", "Blurred vision", "Slow-healing sores", "Frequent infections"],
            "treatments": ["Healthy eating", "Regular exercise", "Weight loss", "Diabetes medications or insulin therapy", "Blood sugar monitoring", "Bariatric surgery"],
            "references": ["American Diabetes Association Standards of Care, 2023", "American Association of Clinical Endocrinologists, 2022"]
        },
        {
            "name": "Osteoporosis",
            "description": "Osteoporosis causes bones to become weak and brittle — so brittle that a fall or even mild stresses such as bending over or coughing can cause a fracture. Osteoporosis-related fractures most commonly occur in the hip, wrist or spine.",
            "symptoms": ["Back pain, caused by a fractured or collapsed vertebra", "Loss of height over time", "A stooped posture", "A bone that breaks much more easily than expected"],
            "treatments": ["Bisphosphonates", "Hormone-related therapy", "Denosumab", "Bone-building medications", "Calcium and vitamin D supplements", "Exercise"],
            "references": ["American Association of Clinical Endocrinologists, 2022", "National Osteoporosis Foundation, 2023"]
        }
    ],
    "medications": [
        {
            "name": "Insulin Glargine",
            "class": "Long-acting insulin",
            "description": "Insulin glargine is a long-acting insulin analog that helps control blood sugar levels in people with diabetes. It provides a steady release of insulin over 24 hours, helping to maintain baseline glucose control.",
            "uses": ["Type 1 Diabetes Mellitus", "Type 2 Diabetes Mellitus"],
            "side_effects": ["Hypoglycemia", "Weight gain", "Injection site reactions", "Allergic reactions", "Lipodystrophy"],
            "dosing": "Individualized dosing, typically once daily at the same time each day.",
            "contraindications": ["Hypersensitivity to insulin glargine", "During episodes of hypoglycemia"]
        },
        {
            "name": "Metformin",
            "class": "Biguanide",
            "description": "Metformin is an oral diabetes medication that helps control blood sugar levels by improving the body's sensitivity to insulin and reducing the amount of glucose produced by the liver. It's the first-line medication for the treatment of type 2 diabetes.",
            "uses": ["Type 2 Diabetes Mellitus"],
            "side_effects": ["Diarrhea", "Nausea", "Vomiting", "Flatulence", "Asthenia", "Vitamin B12 deficiency", "Lactic acidosis (rare)"],
            "dosing": "Initial: 500 mg twice daily or 850 mg once daily with meals. Maximum: 2550 mg/day in divided doses.",
            "contraindications": ["Renal disease or dysfunction", "Acute or chronic metabolic acidosis", "Hypersensitivity to metformin"]
        },
        {
            "name": "Alendronate",
            "class": "Bisphosphonate",
            "description": "Alendronate is a bisphosphonate medication that helps prevent and treat osteoporosis by slowing bone loss and increasing bone density. It works by inhibiting the activity of osteoclasts, the cells that cause bone loss.",
            "uses": ["Osteoporosis"],
            "side_effects": ["Esophageal irritation", "Abdominal pain", "Acid reflux", "Musculoskeletal pain", "Osteonecrosis of the jaw (rare)", "Atypical femur fractures (rare)"],
            "dosing": "Treatment of osteoporosis: 10 mg once daily or 70 mg once weekly. Prevention of osteoporosis: 5 mg once daily or 35 mg once weekly.",
            "contraindications": ["Abnormalities of the esophagus which delay esophageal emptying", "Inability to stand or sit upright for at least 30 minutes", "Hypocalcemia", "Severe renal insufficiency"]
        }
    ]
}

class EndocrinologyDataImporter(BaseDataImporter):
    """Importer for endocrinology data"""
    
    def __init__(self):
        """Initialize the endocrinology data importer"""
        super().__init__(
            specialty_name="Endocrinology",
            specialty_description="Branch of medicine dealing with disorders of the endocrine system, its hormones, and their receptors."
        )
        # The specialty is already created in the base class constructor
    
    def import_data(self):
        """Import all endocrinology data"""
        self.import_conditions()
        self.import_medications()
        self.import_references()
        self.import_guidelines()
        return True
    
    def import_conditions(self):
        """Import endocrinology-specific conditions"""
        conditions = []
        
        for condition_data in ENDOCRINOLOGY_DATA['conditions']:
            condition = self.add_condition(
                name=condition_data['name'],
                description=condition_data['description'],
                symptoms=condition_data['symptoms'],
                treatments=condition_data['treatments'],
                references=[{"title": ref, "url": ""} for ref in condition_data['references']]
            )
            conditions.append(condition)
            
        print(f"Imported {len(conditions)} endocrinology conditions")
        return conditions
    
    def import_medications(self):
        """Import endocrinology-specific medications"""
        medications = []
        
        for medication_data in ENDOCRINOLOGY_DATA['medications']:
            medication = self.add_medication(
                name=medication_data['name'],
                class_name=medication_data['class'],
                description=medication_data['description'],
                uses=medication_data['uses'],
                side_effects=medication_data['side_effects'],
                dosing=medication_data['dosing'],
                contraindications=medication_data['contraindications']
            )
            medications.append(medication)
            
            # Link medication to relevant conditions
            for use in medication_data['uses']:
                self.link_medication_to_condition(medication_data['name'], use)
            
        print(f"Imported {len(medications)} endocrinology medications")
        return medications
    
    def import_references(self):
        """Import endocrinology-specific references"""
        references = [
            {
                "title": "American Diabetes Association",
                "url": "https://diabetes.org/",
                "description": "Organization dedicated to fighting diabetes and improving the lives of all people affected by diabetes."
            },
            {
                "title": "American Association of Clinical Endocrinologists",
                "url": "https://www.aace.com/",
                "description": "Professional community of physicians specializing in endocrinology, diabetes, and metabolism."
            },
            {
                "title": "National Osteoporosis Foundation",
                "url": "https://www.nof.org/",
                "description": "Leading health organization dedicated to preventing osteoporosis and broken bones."
            }
        ]
        
        for reference_data in references:
            self.add_reference(
                title=reference_data["title"],
                url=reference_data["url"],
                description=reference_data.get("description")
            )
        
        print(f"Imported {len(references)} endocrinology references")
    
    def import_guidelines(self):
        """Import endocrinology-specific guidelines"""
        guidelines = [
            {
                "title": "Standards of Medical Care in Diabetes",
                "organization": "American Diabetes Association",
                "publication_year": 2023,
                "url": "https://diabetesjournals.org/care/issue/46/Supplement_1",
                "summary": "Comprehensive, evidence-based recommendations for the diagnosis and treatment of diabetes."
            },
            {
                "title": "Clinical Practice Guidelines for Developing a Diabetes Mellitus Comprehensive Care Plan",
                "organization": "American Association of Clinical Endocrinologists",
                "publication_year": 2022,
                "url": "https://pro.aace.com/disease-state-resources/diabetes/clinical-practice-guidelines",
                "summary": "Guidelines for developing comprehensive care plans for patients with diabetes mellitus."
            },
            {
                "title": "Clinician's Guide to Prevention and Treatment of Osteoporosis",
                "organization": "National Osteoporosis Foundation",
                "publication_year": 2023,
                "url": "https://www.nof.org/patients/diagnosis-information/clinicians-guide-to-the-prevention-and-treatment-of-osteoporosis/",
                "summary": "Evidence-based guidelines for the diagnosis and treatment of osteoporosis."
            }
        ]
        
        for guideline_data in guidelines:
            self.add_guideline(
                title=guideline_data["title"],
                organization=guideline_data["organization"],
                publication_year=guideline_data["publication_year"],
                summary=guideline_data["summary"],
                url=guideline_data.get("url")
            )
        
        print(f"Imported {len(guidelines)} endocrinology guidelines")


if __name__ == "__main__":
    importer = EndocrinologyDataImporter()
    importer.import_data()
