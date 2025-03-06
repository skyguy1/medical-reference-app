"""
Nephrology Data Importer

This module imports nephrology-related conditions and medications
into the medical reference database.
"""
from data_importer_base import BaseDataImporter

class NephrologyDataImporter(BaseDataImporter):
    """
    Importer for nephrology-related medical data
    """
    
    def __init__(self):
        """Initialize the nephrology data importer with specialty information"""
        super().__init__(
            specialty_name="Nephrology",
            specialty_description="Nephrology is a specialty of medicine that focuses on kidney care and treating diseases of the kidneys."
        )
    
    def import_data(self):
        """Import all nephrology data"""
        self.import_conditions()
        self.import_medications()
        self.import_references()
        self.import_guidelines()
        return True
    
    def import_conditions(self):
        """Import nephrology-specific conditions"""
        conditions = [
            {
                "name": "Chronic Kidney Disease (CKD)",
                "description": "Progressive loss of kidney function over time.",
                "symptoms": [
                    "Fatigue", 
                    "Fluid retention", 
                    "Shortness of breath", 
                    "Nausea", 
                    "Decreased appetite",
                    "Sleep problems",
                    "Changes in urine output"
                ],
                "treatments": [
                    "ACE inhibitors or ARBs for blood pressure control",
                    "Dietary restrictions (low sodium, low potassium)",
                    "Management of underlying conditions",
                    "Dialysis (for advanced stages)",
                    "Kidney transplantation (for end-stage renal disease)"
                ],
                "references": [
                    {"title": "KDIGO 2012 Clinical Practice Guideline for CKD", "url": "https://kdigo.org/guidelines/ckd-evaluation-and-management/"},
                    {"title": "National Kidney Foundation: CKD", "url": "https://www.kidney.org/atoz/content/about-chronic-kidney-disease"}
                ]
            },
            {
                "name": "Acute Kidney Injury (AKI)",
                "description": "Sudden decrease in kidney function resulting in the accumulation of waste products in the blood.",
                "symptoms": [
                    "Decreased urine output",
                    "Fluid retention",
                    "Shortness of breath",
                    "Fatigue",
                    "Confusion",
                    "Nausea",
                    "Chest pain or pressure"
                ],
                "treatments": [
                    "Treatment of underlying cause",
                    "Fluid management",
                    "Medication adjustments",
                    "Temporary dialysis if severe",
                    "Avoidance of nephrotoxic agents"
                ],
                "references": [
                    {"title": "KDIGO Clinical Practice Guideline for AKI", "url": "https://kdigo.org/guidelines/acute-kidney-injury/"},
                    {"title": "American Kidney Fund: Acute Kidney Injury", "url": "https://www.kidneyfund.org/kidney-disease/other-kidney-conditions/acute-kidney-injury"}
                ]
            },
            {
                "name": "Nephrotic Syndrome",
                "description": "A kidney disorder characterized by proteinuria, hypoalbuminemia, and edema.",
                "symptoms": [
                    "Severe edema, especially around the eyes and in the legs",
                    "Foamy urine (due to protein)",
                    "Weight gain due to fluid retention",
                    "Fatigue",
                    "Loss of appetite",
                    "Increased susceptibility to infections"
                ],
                "treatments": [
                    "Corticosteroids",
                    "Immunosuppressive agents",
                    "ACE inhibitors or ARBs",
                    "Diuretics",
                    "Dietary modifications (low sodium)",
                    "Treatment of underlying cause"
                ],
                "references": [
                    {"title": "KDIGO Clinical Practice Guideline for Glomerulonephritis", "url": "https://kdigo.org/guidelines/gn/"},
                    {"title": "National Kidney Foundation: Nephrotic Syndrome", "url": "https://www.kidney.org/atoz/content/nephrotic"}
                ]
            },
            {
                "name": "Polycystic Kidney Disease (PKD)",
                "description": "Inherited disorder characterized by the development of clusters of cysts in the kidneys.",
                "symptoms": [
                    "High blood pressure",
                    "Back or side pain",
                    "Blood in urine",
                    "Kidney stones",
                    "Urinary tract infections",
                    "Kidney failure (in advanced stages)"
                ],
                "treatments": [
                    "Blood pressure management",
                    "Pain management",
                    "Treatment of complications (UTIs, kidney stones)",
                    "Tolvaptan (to slow cyst growth in ADPKD)",
                    "Dialysis or kidney transplant (for end-stage renal disease)"
                ],
                "references": [
                    {"title": "PKD Foundation", "url": "https://pkdcure.org/"},
                    {"title": "National Institute of Diabetes and Digestive and Kidney Diseases: PKD", "url": "https://www.niddk.nih.gov/health-information/kidney-disease/polycystic-kidney-disease"}
                ]
            },
            {
                "name": "Glomerulonephritis",
                "description": "Inflammation of the glomeruli, which are tiny structures in the kidneys that filter blood.",
                "symptoms": [
                    "Pink or cola-colored urine (hematuria)",
                    "Foamy urine (proteinuria)",
                    "High blood pressure",
                    "Fluid retention (edema)",
                    "Fatigue",
                    "Decreased urine output"
                ],
                "treatments": [
                    "Corticosteroids",
                    "Immunosuppressive medications",
                    "Plasmapheresis (for certain types)",
                    "Blood pressure medications",
                    "Dietary changes",
                    "Treatment of underlying cause"
                ],
                "references": [
                    {"title": "KDIGO Clinical Practice Guideline for Glomerulonephritis", "url": "https://kdigo.org/guidelines/gn/"},
                    {"title": "National Kidney Foundation: Glomerulonephritis", "url": "https://www.kidney.org/atoz/content/glomerul"}
                ]
            }
        ]
        
        for condition_data in conditions:
            name = condition_data["name"]
            description = condition_data["description"]
            symptoms = condition_data["symptoms"]
            treatments = condition_data["treatments"]
            references = condition_data["references"]
            self.add_condition(name, description, symptoms, treatments, references)
        
        print(f"Imported {len(conditions)} nephrology conditions")
    
    def import_medications(self):
        """Import nephrology-specific medications"""
        medications = [
            {
                "name": "Furosemide (Lasix)",
                "class_name": "Loop diuretic",
                "description": "Furosemide is a loop diuretic that prevents your body from absorbing too much salt, allowing the salt to be passed in your urine. It's used to treat fluid retention and edema in patients with kidney disease, heart failure, or liver disease.",
                "dosage": "20-80 mg daily, can be increased as needed",
                "side_effects": [
                    "Electrolyte imbalances",
                    "Dehydration",
                    "Hypotension",
                    "Ototoxicity with high doses",
                    "Increased blood glucose"
                ],
                "contraindications": [
                    "Anuria",
                    "Severe electrolyte depletion",
                    "Sulfonamide allergy"
                ],
                "references": [
                    {"title": "Furosemide Drug Information", "url": "https://www.ncbi.nlm.nih.gov/books/NBK499921/"}
                ]
            },
            {
                "name": "Lisinopril",
                "class_name": "ACE inhibitor",
                "description": "Lisinopril is an ACE inhibitor that helps relax blood vessels, lowering blood pressure and reducing strain on the heart. It's used to treat hypertension and protect kidney function in chronic kidney disease.",
                "dosage": "5-40 mg once daily",
                "side_effects": [
                    "Dry cough",
                    "Hyperkalemia",
                    "Angioedema",
                    "Hypotension",
                    "Acute kidney injury (in certain settings)"
                ],
                "contraindications": [
                    "History of angioedema",
                    "Pregnancy",
                    "Bilateral renal artery stenosis"
                ],
                "references": [
                    {"title": "ACE Inhibitors in Kidney Disease", "url": "https://www.kidney.org/atoz/content/ace-inhibitors"}
                ]
            },
            {
                "name": "Sevelamer (Renvela)",
                "class_name": "Phosphate binder",
                "description": "Sevelamer is a phosphate binder that helps control phosphate levels in the blood. It's used to treat hyperphosphatemia in patients with chronic kidney disease.",
                "dosage": "800-1600 mg three times daily with meals",
                "side_effects": [
                    "Gastrointestinal discomfort",
                    "Constipation",
                    "Diarrhea",
                    "Nausea",
                    "Vomiting"
                ],
                "contraindications": [
                    "Bowel obstruction",
                    "Hypophosphatemia"
                ],
                "references": [
                    {"title": "KDIGO Clinical Practice Guideline for CKD-MBD", "url": "https://kdigo.org/guidelines/ckd-mbd/"}
                ]
            },
            {
                "name": "Calcitriol (Rocaltrol)",
                "class_name": "Vitamin D analog",
                "description": "Calcitriol is a vitamin D analog that helps regulate calcium and phosphate levels in the blood. It's used to treat secondary hyperparathyroidism in patients with chronic kidney disease.",
                "dosage": "0.25-1 mcg daily or every other day",
                "side_effects": [
                    "Hypercalcemia",
                    "Hyperphosphatemia",
                    "Nausea",
                    "Vomiting",
                    "Constipation"
                ],
                "contraindications": [
                    "Hypercalcemia",
                    "Vitamin D toxicity"
                ],
                "references": [
                    {"title": "KDIGO Clinical Practice Guideline for CKD-MBD", "url": "https://kdigo.org/guidelines/ckd-mbd/"}
                ]
            },
            {
                "name": "Epoetin alfa (Epogen, Procrit)",
                "class_name": "Erythropoiesis-stimulating agent",
                "description": "Epoetin alfa is an erythropoiesis-stimulating agent that helps stimulate red blood cell production. It's used to treat anemia in patients with chronic kidney disease.",
                "dosage": "50-300 units/kg three times weekly, adjusted based on hemoglobin response",
                "side_effects": [
                    "Hypertension",
                    "Increased risk of thrombotic events",
                    "Headache",
                    "Injection site pain",
                    "Pure red cell aplasia (rare)"
                ],
                "contraindications": [
                    "Uncontrolled hypertension",
                    "Known hypersensitivity"
                ],
                "references": [
                    {"title": "KDIGO Clinical Practice Guideline for Anemia in CKD", "url": "https://kdigo.org/guidelines/anemia-in-ckd/"}
                ]
            },
            {
                "name": "Tolvaptan (Jynarque)",
                "class_name": "Vasopressin V2 receptor antagonist",
                "description": "Tolvaptan is a vasopressin V2 receptor antagonist that helps slow kidney function decline in patients with autosomal dominant polycystic kidney disease (ADPKD).",
                "dosage": "60-120 mg daily in divided doses",
                "side_effects": [
                    "Thirst and increased water intake",
                    "Polyuria",
                    "Nocturia",
                    "Potential for liver injury",
                    "Dehydration"
                ],
                "contraindications": [
                    "Liver disease",
                    "Hypovolemia",
                    "Hypernatremia",
                    "Pregnancy"
                ],
                "references": [
                    {"title": "Tolvaptan for ADPKD", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6336216/"}
                ]
            }
        ]
        
        for medication_data in medications:
            name = medication_data["name"]
            class_name = medication_data["class_name"]
            description = medication_data["description"]
            side_effects = medication_data.get("side_effects", [])
            dosing = medication_data.get("dosage", "")
            contraindications = medication_data.get("contraindications", [])
            
            self.add_medication(name, class_name, description, side_effects, dosing, contraindications)
        
        print(f"Imported {len(medications)} nephrology medications")
    
    def import_references(self):
        """Import nephrology-specific references"""
        references = [
            {
                "title": "Kidney Disease: Improving Global Outcomes (KDIGO)",
                "url": "https://kdigo.org/guidelines/",
                "description": "International organization developing and implementing evidence-based clinical practice guidelines in kidney disease."
            },
            {
                "title": "National Kidney Foundation",
                "url": "https://www.kidney.org/professionals",
                "description": "Professional education resources for kidney disease management."
            },
            {
                "title": "American Society of Nephrology",
                "url": "https://www.asn-online.org/",
                "description": "Leading organization dedicated to fighting kidney disease through education, advocacy, and research."
            }
        ]
        
        for reference_data in references:
            title = reference_data["title"]
            url = reference_data.get("url")
            
            self.add_reference(title=title, url=url)
        
        print(f"Imported {len(references)} nephrology references")
    
    def import_guidelines(self):
        """Import nephrology-specific guidelines"""
        guidelines = [
            {
                "title": "KDIGO 2012 Clinical Practice Guideline for the Evaluation and Management of CKD",
                "organization": "Kidney Disease: Improving Global Outcomes",
                "publication_year": 2012,
                "url": "https://kdigo.org/guidelines/ckd-evaluation-and-management/",
                "summary": "Comprehensive guidelines for the diagnosis, evaluation, and management of chronic kidney disease."
            },
            {
                "title": "KDIGO 2021 Clinical Practice Guideline for the Management of Blood Pressure in CKD",
                "organization": "Kidney Disease: Improving Global Outcomes",
                "publication_year": 2021,
                "url": "https://kdigo.org/guidelines/blood-pressure-in-ckd/",
                "summary": "Evidence-based recommendations for blood pressure management in patients with chronic kidney disease."
            },
            {
                "title": "KDIGO Clinical Practice Guideline for Anemia in CKD",
                "organization": "Kidney Disease: Improving Global Outcomes",
                "publication_year": 2012,
                "url": "https://kdigo.org/guidelines/anemia-in-ckd/",
                "summary": "Guidelines for the diagnosis and management of anemia in patients with chronic kidney disease."
            }
        ]
        
        for guideline_data in guidelines:
            title = guideline_data["title"]
            organization = guideline_data["organization"]
            publication_year = guideline_data["publication_year"]
            url = guideline_data.get("url")
            summary = guideline_data.get("summary")
            
            self.add_guideline(title, organization, publication_year, summary, url=url)
        
        print(f"Imported {len(guidelines)} nephrology guidelines")
