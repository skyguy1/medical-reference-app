"""
Rheumatology Data Importer

This module imports rheumatology-related conditions and medications
into the medical reference database.
"""
from data_importer_base import BaseDataImporter

class RheumatologyDataImporter(BaseDataImporter):
    """
    Importer for rheumatology-related medical data
    """
    
    def __init__(self):
        """Initialize the rheumatology data importer with specialty information"""
        super().__init__(
            specialty_name="Rheumatology",
            specialty_description="Rheumatology is a medical specialty that diagnoses and treats rheumatic diseases, which affect the joints, muscles, bones, and sometimes other organs."
        )
        # The specialty is already created or retrieved in the base class constructor
    
    def import_data(self):
        """Import all rheumatology data"""
        self.import_conditions()
        self.import_medications()
        self.import_references()
        self.import_guidelines()
        return True
    
    def import_conditions(self):
        """Import rheumatology-specific conditions"""
        conditions = []
        
        # Rheumatoid Arthritis
        ra = self.add_condition(
            name="Rheumatoid Arthritis",
            description="An autoimmune disease that causes chronic inflammation of the joints and other areas of the body.",
            symptoms=[
                "Joint pain and swelling", 
                "Joint stiffness, especially in the morning", 
                "Fatigue", 
                "Low-grade fever", 
                "Loss of appetite",
                "Rheumatoid nodules",
                "Symmetrical joint involvement"
            ],
            treatments=[
                "Disease-modifying antirheumatic drugs (DMARDs)",
                "Biological agents",
                "JAK inhibitors",
                "Corticosteroids",
                "NSAIDs",
                "Physical therapy",
                "Surgery in severe cases"
            ],
            references=[
                {"title": "American College of Rheumatology: Rheumatoid Arthritis", "url": "https://www.rheumatology.org/I-Am-A/Patient-Caregiver/Diseases-Conditions/Rheumatoid-Arthritis"},
                {"title": "Arthritis Foundation: Rheumatoid Arthritis", "url": "https://www.arthritis.org/diseases/rheumatoid-arthritis"}
            ]
        )
        conditions.append(ra)
        
        # Osteoarthritis
        oa = self.add_condition(
            name="Osteoarthritis",
            description="A degenerative joint disease characterized by the breakdown of joint cartilage and underlying bone.",
            symptoms=[
                "Joint pain", 
                "Stiffness, especially after periods of inactivity", 
                "Decreased range of motion", 
                "Crepitus (cracking or grinding sensation)",
                "Joint swelling",
                "Bone spurs"
            ],
            treatments=[
                "NSAIDs",
                "Acetaminophen",
                "Topical analgesics",
                "Physical therapy",
                "Weight management",
                "Assistive devices",
                "Joint injections",
                "Joint replacement surgery in severe cases"
            ],
            references=[
                {"title": "American College of Rheumatology: Osteoarthritis", "url": "https://www.rheumatology.org/I-Am-A/Patient-Caregiver/Diseases-Conditions/Osteoarthritis"},
                {"title": "Arthritis Foundation: Osteoarthritis", "url": "https://www.arthritis.org/diseases/osteoarthritis"}
            ]
        )
        conditions.append(oa)
        
        # Systemic Lupus Erythematosus
        lupus = self.add_condition(
            name="Systemic Lupus Erythematosus",
            description="A chronic autoimmune disease that can affect various parts of the body, including the skin, joints, kidneys, brain, and other organs.",
            symptoms=[
                "Butterfly-shaped rash on the face", 
                "Photosensitivity", 
                "Joint pain and swelling", 
                "Fatigue",
                "Fever",
                "Chest pain",
                "Hair loss",
                "Raynaud's phenomenon",
                "Kidney problems"
            ],
            treatments=[
                "NSAIDs",
                "Antimalarials (hydroxychloroquine)",
                "Corticosteroids",
                "Immunosuppressants",
                "Biologics",
                "Lifestyle modifications"
            ],
            references=[
                {"title": "American College of Rheumatology: Lupus", "url": "https://www.rheumatology.org/I-Am-A/Patient-Caregiver/Diseases-Conditions/Lupus"},
                {"title": "Lupus Foundation of America", "url": "https://www.lupus.org/"}
            ]
        )
        conditions.append(lupus)
        
        # Gout
        gout = self.add_condition(
            name="Gout",
            description="A form of inflammatory arthritis characterized by recurrent attacks of a red, tender, hot, and swollen joint, caused by elevated levels of uric acid in the blood.",
            symptoms=[
                "Intense joint pain, often in the big toe", 
                "Swelling and redness", 
                "Limited range of motion", 
                "Lingering discomfort",
                "Tophi (uric acid crystal deposits)"
            ],
            treatments=[
                "NSAIDs",
                "Colchicine",
                "Corticosteroids",
                "Xanthine oxidase inhibitors (allopurinol, febuxostat)",
                "Uricosurics",
                "Dietary modifications",
                "Limiting alcohol consumption"
            ],
            references=[
                {"title": "American College of Rheumatology: Gout", "url": "https://www.rheumatology.org/I-Am-A/Patient-Caregiver/Diseases-Conditions/Gout"},
                {"title": "Arthritis Foundation: Gout", "url": "https://www.arthritis.org/diseases/gout"}
            ]
        )
        conditions.append(gout)
        
        # Ankylosing Spondylitis
        as_condition = self.add_condition(
            name="Ankylosing Spondylitis",
            description="A type of arthritis that causes inflammation primarily in the spine, leading to pain and stiffness from the neck to the lower back.",
            symptoms=[
                "Lower back pain and stiffness", 
                "Pain that worsens with rest and improves with activity", 
                "Limited spine mobility", 
                "Fatigue",
                "Posture changes",
                "Eye inflammation (uveitis)",
                "Enthesitis (inflammation where tendons/ligaments attach to bone)"
            ],
            treatments=[
                "NSAIDs",
                "TNF inhibitors",
                "IL-17 inhibitors",
                "Physical therapy",
                "Exercise",
                "Posture training",
                "Surgery in severe cases"
            ],
            references=[
                {"title": "American College of Rheumatology: Ankylosing Spondylitis", "url": "https://www.rheumatology.org/I-Am-A/Patient-Caregiver/Diseases-Conditions/Ankylosing-Spondylitis"},
                {"title": "Spondylitis Association of America", "url": "https://spondylitis.org/"}
            ]
        )
        conditions.append(as_condition)
        
        print(f"Imported {len(conditions)} rheumatology conditions")
        return conditions
    
    def import_medications(self):
        """Import rheumatology-specific medications"""
        medications = [
            {
                "name": "Methotrexate",
                "class_name": "Disease-modifying antirheumatic drug (DMARD)",
                "description": "A disease-modifying antirheumatic drug (DMARD) used to treat rheumatoid arthritis, psoriatic arthritis, and other rheumatic conditions.",
                "dosing": "7.5-25 mg once weekly, oral or subcutaneous",
                "side_effects": [
                    "Nausea and vomiting",
                    "Mouth sores",
                    "Fatigue",
                    "Liver enzyme elevations",
                    "Bone marrow suppression",
                    "Increased risk of infections",
                    "Pulmonary toxicity (rare)"
                ],
                "contraindications": [
                    "Pregnancy",
                    "Breastfeeding",
                    "Alcoholism",
                    "Liver disease",
                    "Immunodeficiency",
                    "Blood dyscrasias"
                ],
                "uses": [
                    "Rheumatoid arthritis",
                    "Psoriatic arthritis",
                    "Juvenile idiopathic arthritis",
                    "Lupus"
                ]
            },
            {
                "name": "Adalimumab (Humira)",
                "class_name": "TNF inhibitor biologic",
                "description": "A TNF inhibitor biologic used to treat rheumatoid arthritis, psoriatic arthritis, ankylosing spondylitis, and other inflammatory conditions.",
                "dosing": "40 mg subcutaneous injection every other week",
                "side_effects": [
                    "Injection site reactions",
                    "Increased risk of infections",
                    "Headache",
                    "Rash",
                    "Reactivation of tuberculosis",
                    "Increased risk of certain cancers",
                    "Demyelinating disorders (rare)"
                ],
                "contraindications": [
                    "Active infection",
                    "Untreated latent tuberculosis",
                    "Moderate to severe heart failure",
                    "Multiple sclerosis or other demyelinating disorders"
                ],
                "uses": [
                    "Rheumatoid arthritis",
                    "Psoriatic arthritis",
                    "Ankylosing spondylitis",
                    "Crohn's disease",
                    "Ulcerative colitis",
                    "Plaque psoriasis"
                ]
            },
            {
                "name": "Hydroxychloroquine (Plaquenil)",
                "class_name": "Antimalarial",
                "description": "An antimalarial drug used to treat rheumatoid arthritis and systemic lupus erythematosus.",
                "dosing": "200-400 mg daily, oral",
                "side_effects": [
                    "Nausea",
                    "Headache",
                    "Dizziness",
                    "Skin rash",
                    "Retinal toxicity (with long-term use)",
                    "QT interval prolongation (rare)"
                ],
                "contraindications": [
                    "Retinal or visual field changes",
                    "Hypersensitivity to 4-aminoquinoline compounds",
                    "Long-term therapy in children"
                ],
                "uses": [
                    "Rheumatoid arthritis",
                    "Systemic lupus erythematosus",
                    "Sjögren's syndrome"
                ]
            },
            {
                "name": "Prednisone",
                "class_name": "Corticosteroid",
                "description": "A corticosteroid used to reduce inflammation in various rheumatic conditions.",
                "dosing": "Varies widely based on condition; typically 5-60 mg daily, with tapering as clinically appropriate",
                "side_effects": [
                    "Weight gain",
                    "Increased appetite",
                    "Mood changes",
                    "Insomnia",
                    "Elevated blood glucose",
                    "Osteoporosis",
                    "Increased risk of infections",
                    "Adrenal suppression",
                    "Cataracts",
                    "Hypertension"
                ],
                "contraindications": [
                    "Systemic fungal infections",
                    "Hypersensitivity to corticosteroids"
                ],
                "uses": [
                    "Rheumatoid arthritis",
                    "Systemic lupus erythematosus",
                    "Polymyalgia rheumatica",
                    "Vasculitis",
                    "Inflammatory myopathies"
                ]
            },
            {
                "name": "Colchicine",
                "class_name": "Anti-inflammatory",
                "description": "An anti-inflammatory medication primarily used to treat gout attacks.",
                "dosing": "0.6 mg once or twice daily for chronic gout; 1.2 mg followed by 0.6 mg one hour later for acute gout",
                "side_effects": [
                    "Diarrhea",
                    "Nausea",
                    "Vomiting",
                    "Abdominal pain",
                    "Bone marrow suppression (with high doses)",
                    "Myopathy (rare)",
                    "Neuropathy (rare)"
                ],
                "contraindications": [
                    "Severe renal impairment",
                    "Severe hepatic impairment",
                    "Concurrent use of P-glycoprotein or CYP3A4 inhibitors in renal/hepatic impairment"
                ],
                "uses": [
                    "Gout",
                    "Familial Mediterranean fever",
                    "Recurrent pericarditis"
                ]
            }
        ]
        
        for medication_data in medications:
            # Extract data from the dictionary
            name = medication_data["name"]
            class_name = medication_data["class_name"]
            uses = medication_data["uses"]
            side_effects = medication_data["side_effects"]
            dosing = medication_data["dosing"]
            contraindications = medication_data["contraindications"]
            
            # Add the medication using the base class method
            self.add_medication(name, class_name, uses, side_effects, dosing, contraindications)
        
        # Link medications to conditions
        self.link_medication_to_condition("Methotrexate", "Rheumatoid Arthritis")
        self.link_medication_to_condition("Methotrexate", "Systemic Lupus Erythematosus")
        
        self.link_medication_to_condition("Adalimumab (Humira)", "Rheumatoid Arthritis")
        self.link_medication_to_condition("Adalimumab (Humira)", "Ankylosing Spondylitis")
        
        self.link_medication_to_condition("Hydroxychloroquine (Plaquenil)", "Rheumatoid Arthritis")
        self.link_medication_to_condition("Hydroxychloroquine (Plaquenil)", "Systemic Lupus Erythematosus")
        
        self.link_medication_to_condition("Prednisone", "Rheumatoid Arthritis")
        self.link_medication_to_condition("Prednisone", "Systemic Lupus Erythematosus")
        
        self.link_medication_to_condition("Colchicine", "Gout")
        
        print(f"Imported {len(medications)} rheumatology medications")
    
    def import_references(self):
        """Import rheumatology-specific references"""
        references = [
            {
                "title": "American College of Rheumatology",
                "url": "https://www.rheumatology.org/",
                "description": "Professional organization of rheumatologists providing resources for healthcare providers and patients."
            },
            {
                "title": "Arthritis Foundation",
                "url": "https://www.arthritis.org/",
                "description": "Nonprofit organization dedicated to addressing the needs of people living with arthritis."
            },
            {
                "title": "Spondylitis Association of America",
                "url": "https://spondylitis.org/",
                "description": "Nonprofit organization dedicated to research, support, and education for ankylosing spondylitis and related diseases."
            }
        ]
        
        for reference_data in references:
            # Extract data from the dictionary
            title = reference_data["title"]
            url = reference_data["url"]
            description = reference_data.get("description")
            
            # Add the reference using the base class method
            self.add_reference(title=title, url=url)
        
        print(f"Imported {len(references)} rheumatology references")
    
    def import_guidelines(self):
        """Import rheumatology-specific guidelines"""
        guidelines = [
            {
                "title": "2021 American College of Rheumatology Guideline for the Treatment of Rheumatoid Arthritis",
                "organization": "American College of Rheumatology",
                "publication_year": 2021,
                "url": "https://www.rheumatology.org/Practice-Quality/Clinical-Support/Clinical-Practice-Guidelines/Rheumatoid-Arthritis",
                "summary": "Evidence-based recommendations for the pharmacological treatment of rheumatoid arthritis."
            },
            {
                "title": "2019 Update of the American College of Rheumatology/Spondylitis Association of America/Spondyloarthritis Research and Treatment Network Recommendations for the Treatment of Ankylosing Spondylitis and Nonradiographic Axial Spondyloarthritis",
                "organization": "American College of Rheumatology, Spondylitis Association of America, Spondyloarthritis Research and Treatment Network",
                "publication_year": 2019,
                "url": "https://www.rheumatology.org/Practice-Quality/Clinical-Support/Clinical-Practice-Guidelines/Axial-Spondyloarthritis",
                "summary": "Recommendations for the treatment of ankylosing spondylitis and nonradiographic axial spondyloarthritis."
            },
            {
                "title": "2020 American College of Rheumatology Guideline for the Management of Gout",
                "organization": "American College of Rheumatology",
                "publication_year": 2020,
                "url": "https://www.rheumatology.org/Practice-Quality/Clinical-Support/Clinical-Practice-Guidelines/Gout",
                "summary": "Evidence-based recommendations for the management of gout."
            }
        ]
        
        for guideline_data in guidelines:
            # Extract data from the dictionary
            title = guideline_data["title"]
            organization = guideline_data["organization"]
            publication_year = guideline_data["publication_year"]
            summary = guideline_data["summary"]
            url = guideline_data.get("url")
            
            # Add the guideline using the base class method
            self.add_guideline(title, organization, publication_year, summary, url=url)
        
        print(f"Imported {len(guidelines)} rheumatology guidelines")


if __name__ == "__main__":
    importer = RheumatologyDataImporter()
    importer.import_data()
