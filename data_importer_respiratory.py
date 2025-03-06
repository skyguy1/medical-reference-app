"""
Respiratory Data Importer

This module imports respiratory-related conditions and medications
into the medical reference database.
"""
from data_importer_base import BaseDataImporter

class RespiratoryDataImporter(BaseDataImporter):
    """
    Importer for respiratory-related medical data
    """
    
    def __init__(self):
        """Initialize the respiratory data importer with specialty information"""
        super().__init__(
            specialty_name="Pulmonology",
            specialty_description="Branch of medicine that deals with diseases of the respiratory tract."
        )
    
    def import_data(self):
        """Import all respiratory data"""
        self.import_conditions()
        self.import_medications()
        return True
    
    def import_conditions(self):
        """Import respiratory-specific conditions"""
        conditions = []
        
        # Asthma
        asthma = self.add_condition(
            name="Asthma",
            description="Asthma is a condition in which your airways narrow and swell and may produce extra mucus. This can make breathing difficult and trigger coughing, a whistling sound (wheezing) when you breathe out and shortness of breath.",
            symptoms=[
                "Shortness of breath", 
                "Chest tightness or pain", 
                "Wheezing when exhaling", 
                "Trouble sleeping caused by shortness of breath", 
                "Coughing or wheezing attacks that are worsened by respiratory virus"
            ],
            treatments=[
                "Inhaled corticosteroids", 
                "Long-acting beta agonists", 
                "Leukotriene modifiers", 
                "Combination inhalers", 
                "Biologics for severe asthma"
            ],
            references=[
                {"title": "Global Initiative for Asthma (GINA) Guidelines, 2023", "url": "https://ginasthma.org/"},
                {"title": "American Thoracic Society, 2022", "url": "https://www.thoracic.org/"}
            ]
        )
        conditions.append(asthma)
        
        # COPD
        copd = self.add_condition(
            name="Chronic Obstructive Pulmonary Disease (COPD)",
            description="Chronic obstructive pulmonary disease (COPD) is a chronic inflammatory lung disease that causes obstructed airflow from the lungs. Symptoms include breathing difficulty, cough, mucus production and wheezing.",
            symptoms=[
                "Shortness of breath, especially during physical activities", 
                "Wheezing", 
                "Chest tightness", 
                "Chronic cough that may produce mucus", 
                "Frequent respiratory infections", 
                "Lack of energy", 
                "Unintended weight loss (in later stages)"
            ],
            treatments=[
                "Bronchodilators", 
                "Inhaled steroids", 
                "Pulmonary rehabilitation", 
                "Oxygen therapy", 
                "Surgery in severe cases"
            ],
            references=[
                {"title": "Global Initiative for Chronic Obstructive Lung Disease (GOLD) Guidelines, 2023", "url": "https://goldcopd.org/"},
                {"title": "American Thoracic Society, 2022", "url": "https://www.thoracic.org/"}
            ]
        )
        conditions.append(copd)
        
        # Pneumonia
        pneumonia = self.add_condition(
            name="Pneumonia",
            description="Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus, causing cough with phlegm or pus, fever, chills, and difficulty breathing.",
            symptoms=[
                "Chest pain when breathing or coughing", 
                "Confusion or changes in mental awareness (in adults age 65 and older)", 
                "Cough, which may produce phlegm", 
                "Fatigue", 
                "Fever, sweating and shaking chills", 
                "Lower than normal body temperature (in adults older than age 65 and people with weak immune systems)", 
                "Nausea, vomiting or diarrhea", 
                "Shortness of breath"
            ],
            treatments=[
                "Antibiotics", 
                "Cough medicine", 
                "Fever reducers/pain relievers", 
                "Hospitalization in severe cases"
            ],
            references=[
                {"title": "Infectious Diseases Society of America/American Thoracic Society Guidelines, 2023", "url": "https://www.thoracic.org/"},
                {"title": "World Health Organization, 2022", "url": "https://www.who.int/"}
            ]
        )
        conditions.append(pneumonia)
        
        # Pulmonary Embolism
        pe = self.add_condition(
            name="Pulmonary Embolism",
            description="Pulmonary embolism is a blockage in one of the pulmonary arteries in your lungs. In most cases, pulmonary embolism is caused by blood clots that travel to the lungs from deep veins in the legs or, rarely, from veins in other parts of the body (deep vein thrombosis).",
            symptoms=[
                "Shortness of breath", 
                "Chest pain that may become worse when breathing deeply", 
                "Cough, which may contain blood", 
                "Rapid or irregular heartbeat", 
                "Lightheadedness or dizziness", 
                "Excessive sweating", 
                "Fever", 
                "Leg pain or swelling, or both, usually in the calf"
            ],
            treatments=[
                "Anticoagulants", 
                "Thrombolytics", 
                "Surgical clot removal", 
                "Vena cava filter"
            ],
            references=[
                {"title": "American College of Chest Physicians Guidelines, 2023", "url": "https://www.chestnet.org/"},
                {"title": "European Society of Cardiology, 2022", "url": "https://www.escardio.org/"}
            ]
        )
        conditions.append(pe)
        
        # Lung Cancer
        lung_cancer = self.add_condition(
            name="Lung Cancer",
            description="Lung cancer is a type of cancer that begins in the lungs. Your lungs are two spongy organs in your chest that take in oxygen when you inhale and release carbon dioxide when you exhale.",
            symptoms=[
                "A new cough that doesn't go away", 
                "Coughing up blood, even a small amount", 
                "Shortness of breath", 
                "Chest pain", 
                "Hoarseness", 
                "Losing weight without trying", 
                "Bone pain", 
                "Headache"
            ],
            treatments=[
                "Surgery", 
                "Chemotherapy", 
                "Radiation therapy", 
                "Targeted drug therapy", 
                "Immunotherapy"
            ],
            references=[
                {"title": "National Comprehensive Cancer Network (NCCN) Guidelines, 2023", "url": "https://www.nccn.org/"},
                {"title": "American Society of Clinical Oncology, 2022", "url": "https://www.asco.org/"}
            ]
        )
        conditions.append(lung_cancer)
        
        print(f"Imported {len(conditions)} respiratory conditions")
        return conditions
    
    def import_medications(self):
        """Import respiratory-specific medications"""
        medications = []
        
        # Albuterol
        albuterol = self.add_medication(
            name="Albuterol",
            class_name="Short-acting beta agonist (SABA)",
            description="Albuterol is a bronchodilator that relaxes muscles in the airways and increases air flow to the lungs. It's primarily used for quick relief of asthma symptoms and to prevent exercise-induced bronchospasm.",
            uses=[
                "Asthma", 
                "COPD", 
                "Exercise-induced bronchoconstriction"
            ],
            side_effects=[
                "Tremor", 
                "Nervousness", 
                "Headache", 
                "Rapid heart rate", 
                "Throat irritation"
            ],
            dosing="2 puffs every 4-6 hours as needed",
            contraindications=[
                "Hypersensitivity to albuterol"
            ]
        )
        medications.append(albuterol)
        
        # Fluticasone
        fluticasone = self.add_medication(
            name="Fluticasone",
            class_name="Inhaled corticosteroid",
            description="Fluticasone is an inhaled corticosteroid that reduces inflammation in the lungs. It's used as a long-term controller medication for asthma and COPD, helping to prevent symptoms and reduce the frequency of attacks.",
            uses=[
                "Asthma", 
                "COPD", 
                "Allergic rhinitis"
            ],
            side_effects=[
                "Oral thrush", 
                "Hoarseness", 
                "Throat irritation", 
                "Cough"
            ],
            dosing="88-880 mcg twice daily depending on severity",
            contraindications=[
                "Hypersensitivity to fluticasone", 
                "Primary treatment of status asthmaticus"
            ]
        )
        medications.append(fluticasone)
        
        # Tiotropium
        tiotropium = self.add_medication(
            name="Tiotropium",
            class_name="Long-acting muscarinic antagonist (LAMA)",
            description="Tiotropium is a long-acting muscarinic antagonist that helps relax the muscles around the airways, making it easier to breathe. It's used to treat COPD and asthma, helping to improve lung function and reduce symptoms.",
            uses=[
                "COPD", 
                "Asthma (off-label)"
            ],
            side_effects=[
                "Dry mouth", 
                "Constipation", 
                "Urinary retention", 
                "Increased intraocular pressure"
            ],
            dosing="18 mcg once daily via inhalation",
            contraindications=[
                "Hypersensitivity to tiotropium", 
                "Hypersensitivity to atropine derivatives"
            ]
        )
        medications.append(tiotropium)
        
        # Azithromycin
        azithromycin = self.add_medication(
            name="Azithromycin",
            class_name="Macrolide antibiotic",
            description="Azithromycin is a macrolide antibiotic that's used to treat various bacterial infections, including community-acquired pneumonia, acute bacterial exacerbation of COPD, and sinusitis.",
            uses=[
                "Community-acquired pneumonia", 
                "Acute bacterial exacerbation of COPD", 
                "Sinusitis", 
                "Pharyngitis"
            ],
            side_effects=[
                "Nausea", 
                "Diarrhea", 
                "Abdominal pain", 
                "QT interval prolongation (rare)"
            ],
            dosing="500 mg on day 1, then 250 mg daily for 4 days",
            contraindications=[
                "Known hypersensitivity", 
                "History of cholestatic jaundice/hepatic dysfunction with azithromycin"
            ]
        )
        medications.append(azithromycin)
        
        # Enoxaparin
        enoxaparin = self.add_medication(
            name="Enoxaparin",
            class_name="Low molecular weight heparin",
            description="Enoxaparin is a low molecular weight heparin that's used to prevent and treat deep vein thrombosis and pulmonary embolism. It works by inhibiting the formation of blood clots.",
            uses=[
                "Pulmonary embolism", 
                "Deep vein thrombosis", 
                "Acute coronary syndrome", 
                "Thromboprophylaxis"
            ],
            side_effects=[
                "Bleeding", 
                "Bruising", 
                "Thrombocytopenia", 
                "Elevated liver enzymes"
            ],
            dosing="1 mg/kg subcutaneously every 12 hours or 1.5 mg/kg once daily for treatment",
            contraindications=[
                "Active major bleeding", 
                "Thrombocytopenia associated with positive in vitro test for anti-platelet antibody"
            ]
        )
        medications.append(enoxaparin)
        
        print(f"Imported {len(medications)} respiratory medications")
        return medications

if __name__ == "__main__":
    importer = RespiratoryDataImporter()
    importer.import_data()
