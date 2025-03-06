"""
Infectious Diseases Data Importer

This module imports infectious disease-related conditions and medications
into the medical reference database.
"""
from data_importer_base import BaseDataImporter

class InfectiousDataImporter(BaseDataImporter):
    """
    Importer for infectious disease-related medical data
    """
    
    def __init__(self):
        """Initialize the infectious diseases data importer with specialty information"""
        super().__init__(
            specialty_name="Infectious Diseases",
            specialty_description="Infectious Diseases is a medical specialty dealing with the diagnosis, control and treatment of infections."
        )
    
    def import_data(self):
        """Import all infectious diseases data"""
        self.import_conditions()
        self.import_medications()
        self.import_references()
        self.import_guidelines()
        return True
    
    def import_conditions(self):
        """Import infectious disease-specific conditions"""
        conditions = []
        
        # Community-Acquired Pneumonia
        cap = self.add_condition(
            name="Community-Acquired Pneumonia",
            description="Community-acquired pneumonia (CAP) is a common infectious disease that is associated with significant morbidity and mortality. It refers to pneumonia acquired outside of hospitals or extended-care facilities.",
            symptoms=[
                "Fever", 
                "Cough with sputum production", 
                "Shortness of breath", 
                "Chest pain", 
                "Fatigue", 
                "Confusion (especially in older adults)", 
                "Nausea, vomiting or diarrhea"
            ],
            treatments=[
                "Antibiotics", 
                "Rest", 
                "Fluids", 
                "Oxygen therapy if needed", 
                "Hospitalization for severe cases"
            ],
            references=[
                {"title": "Infectious Diseases Society of America/American Thoracic Society Guidelines", "url": "https://www.idsociety.org/practice-guideline/community-acquired-pneumonia-cap-in-adults/"},
                {"title": "European Respiratory Society Guidelines", "url": "https://www.ersnet.org/"}
            ]
        )
        conditions.append(cap)
        
        # Urinary Tract Infection
        uti = self.add_condition(
            name="Urinary Tract Infection",
            description="A urinary tract infection (UTI) is an infection in any part of the urinary system, including kidneys, ureters, bladder, and urethra.",
            symptoms=[
                "Burning sensation when urinating", 
                "Frequent urination", 
                "Cloudy, strong-smelling urine", 
                "Pelvic pain in women", 
                "Rectal pain in men", 
                "Fever (if infection has reached kidneys)"
            ],
            treatments=[
                "Antibiotics", 
                "Increased fluid intake", 
                "Urinary analgesics", 
                "Treatment of underlying conditions"
            ],
            references=[
                {"title": "Infectious Diseases Society of America Guidelines", "url": "https://www.idsociety.org/practice-guideline/urinary-tract-infection/"},
                {"title": "American Urological Association", "url": "https://www.auanet.org/"}
            ]
        )
        conditions.append(uti)
        
        # Lyme Disease
        lyme = self.add_condition(
            name="Lyme Disease",
            description="Lyme disease is caused by the bacterium Borrelia burgdorferi and rarely, Borrelia mayonii. It is transmitted to humans through the bite of infected blacklegged ticks.",
            symptoms=[
                "Erythema migrans (bull's-eye rash)", 
                "Fever", 
                "Chills", 
                "Fatigue", 
                "Body aches", 
                "Headache", 
                "Neck stiffness", 
                "Joint pain", 
                "Swollen lymph nodes"
            ],
            treatments=[
                "Antibiotics (doxycycline, amoxicillin, or cefuroxime)", 
                "Treatment of late-stage complications", 
                "Symptomatic relief"
            ],
            references=[
                {"title": "CDC Lyme Disease Information", "url": "https://www.cdc.gov/lyme/"},
                {"title": "Infectious Diseases Society of America Guidelines", "url": "https://www.idsociety.org/practice-guideline/lyme-disease/"}
            ]
        )
        conditions.append(lyme)
        
        # HIV/AIDS
        hiv = self.add_condition(
            name="HIV/AIDS",
            description="Human immunodeficiency virus (HIV) is a virus that attacks the body's immune system. If not treated, it can lead to acquired immunodeficiency syndrome (AIDS).",
            symptoms=[
                "Acute stage: Fever, fatigue, sore throat, swollen lymph nodes, rash", 
                "Clinical latency: Usually asymptomatic", 
                "AIDS: Rapid weight loss, recurring fever, extreme fatigue, prolonged swelling of lymph glands, diarrhea, pneumonia, neurological disorders"
            ],
            treatments=[
                "Antiretroviral therapy (ART)", 
                "Treatment of opportunistic infections", 
                "Preventive measures", 
                "Regular monitoring of CD4 count and viral load"
            ],
            references=[
                {"title": "CDC HIV Information", "url": "https://www.cdc.gov/hiv/"},
                {"title": "World Health Organization HIV Guidelines", "url": "https://www.who.int/health-topics/hiv-aids/"}
            ]
        )
        conditions.append(hiv)
        
        # Tuberculosis
        tb = self.add_condition(
            name="Tuberculosis",
            description="Tuberculosis (TB) is a potentially serious infectious disease that mainly affects the lungs. It is caused by Mycobacterium tuberculosis.",
            symptoms=[
                "Cough (sometimes with blood)", 
                "Weight loss", 
                "Night sweats", 
                "Fever", 
                "Fatigue", 
                "Chest pain", 
                "Loss of appetite"
            ],
            treatments=[
                "Antibiotics (isoniazid, rifampin, ethambutol, pyrazinamide)", 
                "Long-term treatment (6-9 months)", 
                "Directly observed therapy (DOT)", 
                "Treatment of drug-resistant TB"
            ],
            references=[
                {"title": "CDC Tuberculosis Information", "url": "https://www.cdc.gov/tb/"},
                {"title": "World Health Organization TB Guidelines", "url": "https://www.who.int/health-topics/tuberculosis/"}
            ]
        )
        conditions.append(tb)
        
        print(f"Imported {len(conditions)} infectious disease conditions")
        return conditions
    
    def import_medications(self):
        """Import infectious disease-specific medications"""
        medications = [
            {
                "name": "Ceftriaxone",
                "class_name": "Third-generation cephalosporin antibiotic",
                "description": "Ceftriaxone is a third-generation cephalosporin antibiotic with broad-spectrum activity against gram-positive and gram-negative bacteria. It's commonly used to treat severe bacterial infections including pneumonia, meningitis, and gonorrhea.",
                "dosage": "1-2 g IV/IM once daily, depending on the severity of infection",
                "side_effects": [
                    "Diarrhea", 
                    "Nausea", 
                    "Vomiting", 
                    "Rash", 
                    "Pain at injection site", 
                    "Elevated liver enzymes", 
                    "Gallbladder sludging"
                ],
                "contraindications": [
                    "Hypersensitivity to cephalosporins", 
                    "History of anaphylactic reaction to penicillins", 
                    "Neonatal hyperbilirubinemia"
                ],
                "references": [
                    {"title": "Ceftriaxone Drug Information", "url": "https://www.ncbi.nlm.nih.gov/books/NBK470392/"}
                ]
            },
            {
                "name": "Doxycycline",
                "class_name": "Tetracycline antibiotic",
                "description": "Doxycycline is a tetracycline antibiotic that inhibits bacterial protein synthesis. It's effective against a wide range of bacteria and is commonly used to treat Lyme disease, respiratory infections, and certain sexually transmitted infections.",
                "dosage": "100 mg orally twice daily for most infections",
                "side_effects": [
                    "Photosensitivity", 
                    "Nausea", 
                    "Vomiting", 
                    "Diarrhea", 
                    "Esophageal irritation", 
                    "Tooth discoloration (in children)", 
                    "Vaginal candidiasis"
                ],
                "contraindications": [
                    "Pregnancy", 
                    "Children under 8 years", 
                    "Hypersensitivity to tetracyclines", 
                    "Severe hepatic impairment"
                ],
                "references": [
                    {"title": "Doxycycline Drug Information", "url": "https://www.ncbi.nlm.nih.gov/books/NBK555888/"}
                ]
            },
            {
                "name": "Isoniazid",
                "class_name": "Antituberculosis agent",
                "description": "Isoniazid is an antituberculosis agent that inhibits the synthesis of mycolic acid, an essential component of the Mycobacterium tuberculosis cell wall. It's commonly used to treat tuberculosis.",
                "dosage": "5 mg/kg (up to 300 mg) orally once daily for treatment of active TB",
                "side_effects": [
                    "Peripheral neuropathy", 
                    "Hepatotoxicity", 
                    "Rash", 
                    "Nausea", 
                    "Vomiting", 
                    "Fatigue", 
                    "Drug-induced lupus"
                ],
                "contraindications": [
                    "Severe hepatic disease", 
                    "Prior isoniazid-associated hepatic injury", 
                    "Acute liver disease"
                ],
                "references": [
                    {"title": "Isoniazid Drug Information", "url": "https://www.ncbi.nlm.nih.gov/books/NBK556999/"}
                ]
            },
            {
                "name": "Tenofovir/Emtricitabine (Truvada)",
                "class_name": "Nucleoside reverse transcriptase inhibitors",
                "description": "Tenofovir/emtricitabine is a combination antiretroviral medication that inhibits the replication of HIV. It's commonly used to treat HIV infection and prevent HIV transmission.",
                "dosage": "One tablet (containing tenofovir 300 mg and emtricitabine 200 mg) orally once daily",
                "side_effects": [
                    "Nausea", 
                    "Headache", 
                    "Fatigue", 
                    "Renal impairment", 
                    "Decreased bone mineral density", 
                    "Lactic acidosis (rare)"
                ],
                "contraindications": [
                    "Severe renal impairment", 
                    "Hypersensitivity to components", 
                    "Not for use as PrEP in individuals with unknown or positive HIV status"
                ],
                "references": [
                    {"title": "Truvada Drug Information", "url": "https://www.ncbi.nlm.nih.gov/books/NBK459327/"}
                ]
            },
            {
                "name": "Oseltamivir (Tamiflu)",
                "class_name": "Neuraminidase inhibitors",
                "description": "Oseltamivir is a neuraminidase inhibitor that blocks the replication of influenza virus. It's commonly used to treat and prevent influenza A and B.",
                "dosage": "75 mg orally twice daily for 5 days for treatment; 75 mg once daily for prophylaxis",
                "side_effects": [
                    "Nausea", 
                    "Vomiting", 
                    "Headache", 
                    "Diarrhea", 
                    "Dizziness", 
                    "Insomnia", 
                    "Behavioral changes (rare)"
                ],
                "contraindications": [
                    "Hypersensitivity to oseltamivir or any component", 
                    "Dose adjustment needed in renal impairment"
                ],
                "references": [
                    {"title": "Oseltamivir Drug Information", "url": "https://www.ncbi.nlm.nih.gov/books/NBK548586/"}
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
        
        # Link medications to conditions
        self.link_medication_to_condition("Ceftriaxone", "Community-Acquired Pneumonia")
        self.link_medication_to_condition("Doxycycline", "Lyme Disease")
        self.link_medication_to_condition("Isoniazid", "Tuberculosis")
        self.link_medication_to_condition("Tenofovir/Emtricitabine (Truvada)", "HIV/AIDS")
        self.link_medication_to_condition("Oseltamivir (Tamiflu)", "Community-Acquired Pneumonia")
        
        print(f"Imported {len(medications)} infectious disease medications")
    
    def import_references(self):
        """Import infectious disease-specific references"""
        references = [
            {
                "title": "Infectious Diseases Society of America (IDSA)",
                "url": "https://www.idsociety.org/",
                "description": "Professional organization that represents physicians, scientists, and other health care professionals who specialize in infectious diseases."
            },
            {
                "title": "Centers for Disease Control and Prevention (CDC)",
                "url": "https://www.cdc.gov/",
                "description": "National public health institute that provides information on infectious diseases and other health threats."
            },
            {
                "title": "World Health Organization (WHO) - Infectious Diseases",
                "url": "https://www.who.int/health-topics/infectious-diseases",
                "description": "Global health organization providing guidelines and information on infectious diseases worldwide."
            }
        ]
        
        for reference_data in references:
            title = reference_data["title"]
            url = reference_data.get("url")
            
            self.add_reference(title=title, url=url)
        
        print(f"Imported {len(references)} infectious disease references")
    
    def import_guidelines(self):
        """Import infectious disease-specific guidelines"""
        guidelines = [
            {
                "title": "IDSA Guidelines for the Treatment of Community-Acquired Pneumonia",
                "organization": "Infectious Diseases Society of America",
                "publication_year": 2019,
                "url": "https://www.idsociety.org/practice-guideline/community-acquired-pneumonia-cap-in-adults/",
                "summary": "Evidence-based recommendations for the diagnosis and treatment of community-acquired pneumonia in adults."
            },
            {
                "title": "IDSA Guidelines for the Management of HIV/AIDS",
                "organization": "Infectious Diseases Society of America",
                "publication_year": 2020,
                "url": "https://www.idsociety.org/practice-guideline/hiv-aids/",
                "summary": "Comprehensive guidelines for the management of HIV infection, including antiretroviral therapy and opportunistic infections."
            },
            {
                "title": "CDC Guidelines for Tuberculosis Treatment",
                "organization": "Centers for Disease Control and Prevention",
                "publication_year": 2020,
                "url": "https://www.cdc.gov/tb/publications/guidelines/treatment.htm",
                "summary": "Recommendations for the treatment of tuberculosis, including drug regimens and monitoring."
            }
        ]
        
        for guideline_data in guidelines:
            title = guideline_data["title"]
            organization = guideline_data["organization"]
            publication_year = guideline_data["publication_year"]
            url = guideline_data.get("url")
            summary = guideline_data.get("summary")
            
            self.add_guideline(title, organization, publication_year, summary, url=url)
        
        print(f"Imported {len(guidelines)} infectious disease guidelines")

if __name__ == "__main__":
    importer = InfectiousDataImporter()
    importer.import_data()
