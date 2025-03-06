"""
Data importer for dermatology conditions and medications
"""
import json
from models import db, Condition, Medication, Specialty, Reference, Guideline
from data_importer_base import BaseDataImporter

# Dermatology conditions and medications data
DERMATOLOGY_DATA = {
    "conditions": [
        {
            "name": "Psoriasis",
            "description": "Psoriasis is a chronic skin disorder that causes cells to build up rapidly on the surface of the skin, forming itchy, dry, red patches and thick, silvery scales. It is thought to be an immune system problem that causes the skin to regenerate at faster than normal rates.",
            "symptoms": ["Red patches of skin covered with thick, silvery scales", "Small scaling spots", "Dry, cracked skin that may bleed", "Itching, burning or soreness", "Thickened, pitted or ridged nails", "Swollen and stiff joints"],
            "treatments": ["Topical treatments", "Light therapy", "Systemic medications", "Biologics", "Lifestyle modifications"],
            "references": ["American Academy of Dermatology Guidelines, 2023", "National Psoriasis Foundation, 2022"]
        },
        {
            "name": "Atopic Dermatitis",
            "description": "Atopic dermatitis (eczema) is a condition that makes your skin red and itchy. It's common in children but can occur at any age. Atopic dermatitis is long lasting (chronic) and tends to flare periodically.",
            "symptoms": ["Dry skin", "Itching, which may be severe, especially at night", "Red to brownish-gray patches", "Small, raised bumps", "Thickened, cracked, scaly skin", "Raw, sensitive, swollen skin from scratching"],
            "treatments": ["Moisturizers", "Topical corticosteroids", "Topical calcineurin inhibitors", "Oral antihistamines", "Phototherapy", "Systemic immunosuppressants", "Biologics"],
            "references": ["American Academy of Dermatology Guidelines, 2023", "National Eczema Association, 2022"]
        },
        {
            "name": "Acne Vulgaris",
            "description": "Acne vulgaris is a common skin condition that occurs when hair follicles become plugged with oil and dead skin cells. It causes whiteheads, blackheads or pimples. Acne is most common among teenagers, though it affects people of all ages.",
            "symptoms": ["Whiteheads (closed plugged pores)", "Blackheads (open plugged pores)", "Small red, tender bumps (papules)", "Pimples (pustules)", "Large, solid, painful lumps beneath the surface of the skin (nodules)", "Painful, pus-filled lumps beneath the surface of the skin (cystic lesions)"],
            "treatments": ["Topical treatments (benzoyl peroxide, retinoids, antibiotics)", "Oral antibiotics", "Oral isotretinoin", "Oral contraceptives (for women)", "Spironolactone (for women)", "Procedural therapies"],
            "references": ["American Academy of Dermatology Guidelines, 2023", "Global Alliance to Improve Outcomes in Acne, 2022"]
        },
        {
            "name": "Rosacea",
            "description": "Rosacea is a common skin condition that causes redness and visible blood vessels in your face. It may also produce small, red, pus-filled bumps. These signs and symptoms may flare up for weeks to months and then diminish for a while.",
            "symptoms": ["Facial redness", "Swollen red bumps", "Eye problems", "Enlarged nose", "Visible blood vessels on the face"],
            "treatments": ["Topical medications", "Oral antibiotics", "Isotretinoin", "Laser therapy", "Lifestyle modifications"],
            "references": ["American Academy of Dermatology Guidelines, 2023", "National Rosacea Society, 2022"]
        },
        {
            "name": "Melanoma",
            "description": "Melanoma, the most serious type of skin cancer, develops in the cells (melanocytes) that produce melanin — the pigment that gives your skin its color. Melanoma can also form in your eyes and, rarely, inside your body, such as in your nose or throat.",
            "symptoms": ["A change in an existing mole", "Development of a new pigmented or unusual-looking growth on your skin", "Asymmetrical shape", "Irregular border", "Changes in color", "Diameter larger than 6 mm", "Evolving size, shape or color"],
            "treatments": ["Surgery", "Immunotherapy", "Targeted therapy", "Radiation therapy", "Chemotherapy"],
            "references": ["American Academy of Dermatology Guidelines, 2023", "National Comprehensive Cancer Network, 2022"]
        },
        {
            "name": "Cellulitis",
            "description": "Cellulitis is a common, potentially serious bacterial skin infection. The affected skin appears swollen and red and is typically painful and warm to the touch. Cellulitis usually affects the skin on the lower legs, but it can occur in the face, arms and other areas.",
            "symptoms": ["Red area of skin that tends to expand", "Swelling", "Tenderness", "Pain", "Warmth", "Fever", "Red spots", "Blisters", "Skin dimpling"],
            "treatments": ["Antibiotics", "Pain relievers", "Elevation of affected area", "Hospitalization for severe cases"],
            "references": ["Infectious Diseases Society of America Guidelines, 2023", "American Academy of Dermatology, 2022"]
        }
    ],
    "medications": [
        {
            "name": "Adalimumab",
            "class": "Biologic (TNF inhibitor)",
            "description": "Adalimumab is a tumor necrosis factor (TNF) inhibitor that reduces inflammation by blocking TNF-alpha, a protein that promotes inflammation. It's used to treat various inflammatory conditions including psoriasis, rheumatoid arthritis, and inflammatory bowel diseases.",
            "uses": ["Psoriasis", "Rheumatoid arthritis", "Psoriatic arthritis", "Ankylosing spondylitis", "Crohn's disease", "Ulcerative colitis"],
            "side_effects": ["Injection site reactions", "Increased risk of infections", "Headache", "Rash", "Nausea", "Increased risk of certain cancers", "Reactivation of tuberculosis"],
            "dosing": "40 mg subcutaneously every other week",
            "contraindications": ["Active infection", "Hypersensitivity to adalimumab", "Moderate to severe heart failure"]
        },
        {
            "name": "Tacrolimus Ointment",
            "class": "Topical calcineurin inhibitor",
            "description": "Tacrolimus ointment is a topical immunosuppressant that works by inhibiting calcineurin, an enzyme involved in T-cell activation. It's primarily used to treat atopic dermatitis (eczema) by reducing inflammation and itching in the skin.",
            "uses": ["Atopic Dermatitis"],
            "side_effects": ["Burning sensation", "Itching", "Skin redness", "Headache", "Flu-like symptoms", "Increased risk of skin infections"],
            "dosing": "Apply 0.03% or 0.1% ointment to affected areas twice daily",
            "contraindications": ["Hypersensitivity to tacrolimus", "Netherton's syndrome", "Application to infected areas"]
        },
        {
            "name": "Isotretinoin",
            "class": "Retinoid",
            "description": "Isotretinoin is a powerful retinoid medication derived from vitamin A that reduces sebum production, prevents clogged pores, and reduces inflammation. It's primarily used for severe, cystic acne that hasn't responded to other treatments.",
            "uses": ["Acne Vulgaris", "Rosacea", "Psoriasis (severe)", "Ichthyosis"],
            "side_effects": ["Dry lips, skin, and eyes", "Nosebleeds", "Joint and muscle pain", "Elevated triglycerides and cholesterol", "Liver enzyme abnormalities", "Teratogenicity (severe birth defects)"],
            "dosing": "0.5-1 mg/kg/day orally in two divided doses for 15-20 weeks",
            "contraindications": ["Pregnancy", "Breastfeeding", "Hypersensitivity to isotretinoin", "Hypervitaminosis A"]
        },
        {
            "name": "Doxycycline",
            "class": "Tetracycline antibiotic",
            "description": "Doxycycline is a tetracycline antibiotic that works by inhibiting bacterial protein synthesis. In dermatology, it's used to treat acne and rosacea due to both its antimicrobial properties and anti-inflammatory effects.",
            "uses": ["Acne Vulgaris", "Rosacea", "Lyme Disease", "Respiratory infections", "Malaria prophylaxis"],
            "side_effects": ["Photosensitivity", "Nausea", "Vomiting", "Diarrhea", "Esophageal irritation", "Tooth discoloration (in children)"],
            "dosing": "50-100 mg orally once or twice daily for acne and rosacea",
            "contraindications": ["Hypersensitivity to tetracyclines", "Pregnancy", "Children under 8 years", "Severe hepatic impairment"]
        },
        {
            "name": "Pembrolizumab",
            "class": "Monoclonal antibody (PD-1 inhibitor)",
            "description": "Pembrolizumab is an immunotherapy medication that works by blocking the PD-1 pathway, helping the immune system recognize and attack cancer cells. It's used to treat various cancers, including advanced melanoma.",
            "uses": ["Melanoma", "Non-small cell lung cancer", "Head and neck squamous cell carcinoma", "Hodgkin lymphoma", "Urothelial carcinoma"],
            "side_effects": ["Fatigue", "Rash", "Diarrhea", "Nausea", "Pruritus", "Immune-mediated adverse reactions (pneumonitis, colitis, hepatitis, nephritis, endocrinopathies)"],
            "dosing": "200 mg IV every 3 weeks or 400 mg IV every 6 weeks",
            "contraindications": ["Hypersensitivity to pembrolizumab"]
        },
        {
            "name": "Cephalexin",
            "class": "First-generation cephalosporin",
            "description": "Cephalexin is a first-generation cephalosporin antibiotic that works by inhibiting bacterial cell wall synthesis. In dermatology, it's commonly used to treat skin and soft tissue infections, including cellulitis.",
            "uses": ["Cellulitis", "Skin and soft tissue infections", "Urinary tract infections", "Respiratory infections", "Bone infections"],
            "side_effects": ["Diarrhea", "Nausea", "Vomiting", "Abdominal pain", "Rash", "Allergic reactions"],
            "dosing": "250-1000 mg orally every 6 hours",
            "contraindications": ["Hypersensitivity to cephalosporins", "History of anaphylactic reaction to penicillins"]
        }
    ]
}

class DermatologyDataImporter(BaseDataImporter):
    """Importer for dermatology data"""
    
    def __init__(self):
        """Initialize the dermatology data importer"""
        super().__init__(
            specialty_name="Dermatology",
            specialty_description="Branch of medicine dealing with the skin and its diseases."
        )
        # The specialty is already created in the base class constructor
    
    def import_data(self):
        """Import all dermatology data"""
        self.import_conditions()
        self.import_medications()
        self.import_references()
        self.import_guidelines()
        return True
    
    def import_conditions(self):
        """Import dermatology-specific conditions"""
        conditions = []
        
        for condition_data in DERMATOLOGY_DATA['conditions']:
            condition = self.add_condition(
                name=condition_data['name'],
                description=condition_data['description'],
                symptoms=condition_data['symptoms'],
                treatments=condition_data['treatments'],
                references=[{"title": ref, "url": ""} for ref in condition_data['references']]
            )
            conditions.append(condition)
            
        print(f"Imported {len(conditions)} dermatology conditions")
        return conditions
    
    def import_medications(self):
        """Import dermatology-specific medications"""
        medications = []
        
        for medication_data in DERMATOLOGY_DATA['medications']:
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
            
        print(f"Imported {len(medications)} dermatology medications")
        return medications
    
    def import_references(self):
        """Import dermatology-specific references"""
        references = [
            {
                "title": "American Academy of Dermatology",
                "url": "https://www.aad.org/",
                "description": "Professional organization for dermatologists providing resources and guidelines for skin conditions."
            },
            {
                "title": "National Psoriasis Foundation",
                "url": "https://www.psoriasis.org/",
                "description": "Nonprofit organization dedicated to finding a cure for psoriasis and improving the lives of those affected."
            },
            {
                "title": "National Eczema Association",
                "url": "https://nationaleczema.org/",
                "description": "Nonprofit organization dedicated to improving the health and quality of life for individuals with eczema."
            }
        ]
        
        for reference_data in references:
            self.add_reference(
                title=reference_data["title"],
                url=reference_data["url"],
                description=reference_data.get("description")
            )
        
        print(f"Imported {len(references)} dermatology references")
    
    def import_guidelines(self):
        """Import dermatology-specific guidelines"""
        guidelines = [
            {
                "title": "Guidelines of care for the management of psoriasis and psoriatic arthritis",
                "organization": "American Academy of Dermatology",
                "publication_year": 2023,
                "url": "https://www.aad.org/member/clinical-quality/guidelines/psoriasis",
                "summary": "Evidence-based recommendations for the treatment and management of psoriasis and psoriatic arthritis."
            },
            {
                "title": "Guidelines of care for the management of atopic dermatitis",
                "organization": "American Academy of Dermatology",
                "publication_year": 2022,
                "url": "https://www.aad.org/member/clinical-quality/guidelines/atopic-dermatitis",
                "summary": "Evidence-based recommendations for the diagnosis and treatment of atopic dermatitis."
            },
            {
                "title": "Practice Guidelines for the Diagnosis and Management of Skin and Soft Tissue Infections",
                "organization": "Infectious Diseases Society of America",
                "publication_year": 2023,
                "url": "https://www.idsociety.org/practice-guideline/skin-and-soft-tissue-infections/",
                "summary": "Guidelines for the diagnosis and management of skin and soft tissue infections, including cellulitis."
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
        
        print(f"Imported {len(guidelines)} dermatology guidelines")


if __name__ == "__main__":
    importer = DermatologyDataImporter()
    importer.import_data()
