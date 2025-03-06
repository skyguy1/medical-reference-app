"""
Cardiology Data Importer

This module imports cardiology-related conditions and medications
into the medical reference database.
"""
from data_importer_base import BaseDataImporter
from models import Reference

class CardiologyDataImporter(BaseDataImporter):
    """
    Importer for cardiology-related medical data
    """
    
    def __init__(self):
        """Initialize the cardiology data importer with specialty information"""
        super().__init__(
            specialty_name="Cardiology",
            specialty_description="Cardiology is the medical specialty that deals with disorders of the heart and cardiovascular system."
        )
    
    def import_data(self):
        """Import all cardiology data"""
        self.import_conditions()
        self.import_medications()
        self.import_references()
        self.import_guidelines()
        return True
    
    def import_conditions(self):
        """Import cardiology-specific conditions"""
        conditions = [
            {
                "name": "Hypertension",
                "description": "High blood pressure is a common condition in which the long-term force of the blood against your artery walls is high enough that it may eventually cause health problems, such as heart disease.",
                "symptoms": [
                    "Headaches", 
                    "Shortness of breath", 
                    "Nosebleeds"
                ],
                "treatments": [
                    "Lifestyle changes", 
                    "Medication", 
                    "Regular monitoring"
                ],
                "references": [
                    {"title": "JNC 8 Guidelines", "url": "https://jamanetwork.com/journals/jama/fullarticle/1791497"},
                    {"title": "American Heart Association, 2023", "url": "https://www.heart.org/en/health-topics/high-blood-pressure"}
                ]
            },
            {
                "name": "Coronary Artery Disease",
                "description": "Coronary artery disease is a condition in which the major blood vessels that supply your heart become damaged or diseased, often due to cholesterol-containing deposits (plaques) or inflammation.",
                "symptoms": [
                    "Chest pain (angina)", 
                    "Shortness of breath", 
                    "Pain in the neck, jaw, throat, upper abdomen or back", 
                    "Nausea", 
                    "Fatigue"
                ],
                "treatments": [
                    "Lifestyle changes", 
                    "Medications", 
                    "Procedures to restore blood flow", 
                    "Cardiac rehabilitation"
                ],
                "references": [
                    {"title": "American Heart Association, 2023", "url": "https://www.heart.org/en/health-topics/coronary-artery-disease"},
                    {"title": "American College of Cardiology, 2022", "url": "https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2022/04/20/21/23/2022-aha-acc-aacvpr-chest-hfsa-ishr"}
                ]
            },
            {
                "name": "Heart Failure",
                "description": "Heart failure occurs when the heart muscle doesn't pump blood as well as it should. This can lead to fatigue, shortness of breath, and fluid buildup.",
                "symptoms": [
                    "Shortness of breath", 
                    "Fatigue and weakness", 
                    "Swelling in legs, ankles and feet", 
                    "Rapid or irregular heartbeat", 
                    "Reduced ability to exercise"
                ],
                "treatments": [
                    "Medications", 
                    "Lifestyle changes", 
                    "Devices to help your heart work better", 
                    "Surgery"
                ],
                "references": [
                    {"title": "American Heart Association Heart Failure Guidelines", "url": "https://www.heart.org/en/health-topics/heart-failure"},
                    {"title": "Heart Failure Society of America", "url": "https://hfsa.org/patient-hub"}
                ]
            },
            {
                "name": "Atrial Fibrillation",
                "description": "Atrial fibrillation is an irregular and often rapid heart rate that can increase your risk of strokes, heart failure and other heart-related complications.",
                "symptoms": [
                    "Palpitations", 
                    "Weakness", 
                    "Reduced ability to exercise", 
                    "Fatigue", 
                    "Lightheadedness", 
                    "Dizziness", 
                    "Shortness of breath", 
                    "Chest pain"
                ],
                "treatments": [
                    "Medications to control heart rate", 
                    "Medications to prevent blood clots", 
                    "Cardioversion", 
                    "Catheter ablation", 
                    "Surgical maze procedure"
                ],
                "references": [
                    {"title": "American Heart Association Atrial Fibrillation", "url": "https://www.heart.org/en/health-topics/atrial-fibrillation"},
                    {"title": "Heart Rhythm Society", "url": "https://www.hrsonline.org/patient-resources"}
                ]
            },
            {
                "name": "Valvular Heart Disease",
                "description": "Valvular heart disease occurs when any of the heart's valves don't work properly, affecting blood flow through the heart to the body.",
                "symptoms": [
                    "Fatigue", 
                    "Shortness of breath", 
                    "Irregular heartbeat", 
                    "Swollen feet or ankles", 
                    "Chest pain", 
                    "Fainting"
                ],
                "treatments": [
                    "Medications", 
                    "Balloon valvuloplasty", 
                    "Valve repair", 
                    "Valve replacement"
                ],
                "references": [
                    {"title": "American Heart Association Valvular Heart Disease", "url": "https://www.heart.org/en/health-topics/heart-valve-problems-and-disease"},
                    {"title": "ACC/AHA Guidelines for the Management of Patients With Valvular Heart Disease", "url": "https://www.ahajournals.org/doi/10.1161/CIR.0000000000000932"}
                ]
            }
        ]
        
        for condition_data in conditions:
            self.add_condition(
                name=condition_data["name"],
                description=condition_data["description"],
                symptoms=condition_data["symptoms"],
                treatments=condition_data["treatments"],
                references=condition_data["references"]
            )
    
    def import_medications(self):
        """Import cardiology-specific medications"""
        medications = [
            {
                "name": "Lisinopril",
                "class_name": "ACE inhibitor",
                "description": "Lisinopril is an angiotensin-converting enzyme (ACE) inhibitor that helps relax blood vessels, lowering blood pressure and reducing strain on the heart. It's commonly used to treat hypertension, heart failure, and to improve survival after heart attacks.",
                "uses": [
                    "Hypertension", 
                    "Heart failure", 
                    "Post-myocardial infarction"
                ],
                "side_effects": [
                    "Dry cough", 
                    "Dizziness", 
                    "Headache", 
                    "Elevated potassium levels"
                ],
                "dosing": "10-40 mg once daily",
                "contraindications": [
                    "Pregnancy", 
                    "History of angioedema", 
                    "Bilateral renal artery stenosis"
                ],
                "references": [
                    {"title": "ACE Inhibitors in Hypertension: A Guide for General Practitioners", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3068773/"}
                ]
            },
            {
                "name": "Atorvastatin",
                "class_name": "HMG-CoA reductase inhibitor (statin)",
                "description": "Atorvastatin is a statin medication that lowers cholesterol levels by blocking an enzyme in the liver that produces cholesterol. It helps reduce the risk of heart attack, stroke, and other cardiovascular complications in people with heart disease or risk factors.",
                "uses": [
                    "Hyperlipidemia", 
                    "Prevention of cardiovascular disease", 
                    "Coronary artery disease"
                ],
                "side_effects": [
                    "Muscle pain", 
                    "Liver enzyme elevation", 
                    "Headache", 
                    "Digestive problems"
                ],
                "dosing": "10-80 mg once daily",
                "contraindications": [
                    "Active liver disease", 
                    "Pregnancy", 
                    "Breastfeeding"
                ],
                "references": [
                    {"title": "Statin Safety and Associated Adverse Events: A Scientific Statement From the American Heart Association", "url": "https://www.ahajournals.org/doi/10.1161/ATV.0000000000000073"}
                ]
            },
            {
                "name": "Metoprolol",
                "class_name": "Beta-blocker",
                "description": "Metoprolol is a beta-blocker medication that reduces the workload of the heart and opens blood vessels, causing the heart to beat slower and with less force. It's commonly used to treat hypertension, angina, heart failure, and to improve survival after heart attacks.",
                "uses": [
                    "Hypertension", 
                    "Angina", 
                    "Heart failure", 
                    "Post-myocardial infarction"
                ],
                "side_effects": [
                    "Fatigue", 
                    "Dizziness", 
                    "Bradycardia", 
                    "Hypotension"
                ],
                "dosing": "25-200 mg daily in divided doses",
                "contraindications": [
                    "Severe bradycardia", 
                    "Heart block greater than first degree", 
                    "Cardiogenic shock", 
                    "Decompensated heart failure"
                ],
                "references": [
                    {"title": "Beta-Blockers in Cardiovascular Medicine", "url": "https://www.ahajournals.org/doi/10.1161/JAHA.116.004879"}
                ]
            },
            {
                "name": "Warfarin",
                "class_name": "Anticoagulant",
                "description": "Warfarin is an anticoagulant medication that helps prevent blood clots from forming or growing. It's commonly used to treat atrial fibrillation, deep vein thrombosis, pulmonary embolism, and to prevent stroke in people with mechanical heart valves.",
                "uses": [
                    "Atrial fibrillation", 
                    "Deep vein thrombosis", 
                    "Pulmonary embolism", 
                    "Mechanical heart valves"
                ],
                "side_effects": [
                    "Bleeding", 
                    "Bruising", 
                    "Rare skin necrosis"
                ],
                "dosing": "Individualized based on INR (2-3 for most indications)",
                "contraindications": [
                    "Active bleeding", 
                    "Severe liver disease", 
                    "Pregnancy (relative)"
                ],
                "references": [
                    {"title": "Oral Anticoagulation Therapy: Management in the Periprocedural Period", "url": "https://www.aafp.org/pubs/afp/issues/2016/0601/p966.html"}
                ]
            },
            {
                "name": "Amlodipine",
                "class_name": "Calcium channel blocker",
                "description": "Amlodipine is a calcium channel blocker medication that helps relax blood vessels, reducing blood pressure and increasing the supply of blood and oxygen to the heart. It's commonly used to treat hypertension, angina, and coronary artery disease.",
                "uses": [
                    "Hypertension", 
                    "Angina", 
                    "Coronary artery disease"
                ],
                "side_effects": [
                    "Peripheral edema", 
                    "Headache", 
                    "Flushing", 
                    "Dizziness"
                ],
                "dosing": "2.5-10 mg once daily",
                "contraindications": [
                    "Severe hypotension", 
                    "Advanced aortic stenosis"
                ],
                "references": [
                    {"title": "Calcium Channel Blockers in Cardiovascular Pharmacotherapy", "url": "https://www.ahajournals.org/doi/10.1161/JAHA.119.015628"}
                ]
            }
        ]
        
        for medication_data in medications:
            med = self.add_medication(
                name=medication_data["name"],
                class_name=medication_data["class_name"],
                description=medication_data["description"],
                uses=medication_data["uses"],
                side_effects=medication_data["side_effects"],
                dosing=medication_data["dosing"],
                contraindications=medication_data["contraindications"]
            )
            
            # Add references to medication
            if med and "references" in medication_data:
                for ref_data in medication_data["references"]:
                    ref = self.add_reference(
                        title=ref_data["title"],
                        url=ref_data.get("url"),
                        authors=ref_data.get("authors"),
                        publication=ref_data.get("publication"),
                        year=ref_data.get("year"),
                        doi=ref_data.get("doi")
                    )
                    if ref:
                        med.references.append(ref)
        
        # Link medications to conditions
        self.link_medication_to_condition("Lisinopril", "Hypertension")
        self.link_medication_to_condition("Lisinopril", "Heart Failure")
        self.link_medication_to_condition("Metoprolol", "Hypertension")
        self.link_medication_to_condition("Metoprolol", "Heart Failure")
        self.link_medication_to_condition("Metoprolol", "Arrhythmias")
        self.link_medication_to_condition("Amlodipine", "Hypertension")
        self.link_medication_to_condition("Amlodipine", "Angina")
        
        return medications
    
    def import_references(self):
        """Import cardiology-specific references"""
        references = [
            {
                "title": "2023 ACC/AHA Guideline for the Management of Heart Failure",
                "url": "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001063",
                "authors": "Writing Committee Members",
                "publication": "Circulation",
                "year": 2023
            },
            {
                "title": "2019 ACC/AHA Guideline on the Primary Prevention of Cardiovascular Disease",
                "url": "https://www.ahajournals.org/doi/10.1161/CIR.0000000000000678",
                "authors": "Arnett DK, et al.",
                "publication": "Circulation",
                "year": 2019
            },
            {
                "title": "2020 ESC Guidelines for the management of acute coronary syndromes in patients presenting without persistent ST-segment elevation",
                "url": "https://academic.oup.com/eurheartj/article/42/14/1289/5898842",
                "authors": "Collet JP, et al.",
                "publication": "European Heart Journal",
                "year": 2020
            }
        ]
        
        for reference_data in references:
            self.add_reference(
                title=reference_data["title"],
                url=reference_data.get("url"),
                authors=reference_data.get("authors"),
                publication=reference_data.get("publication"),
                year=reference_data.get("year"),
                doi=reference_data.get("doi")
            )
    
    def import_guidelines(self):
        """Import cardiology-specific guidelines"""
        guidelines = [
            {
                "title": "Hypertension Management Guidelines",
                "content": "1. Initial evaluation should include assessment for target organ damage and cardiovascular risk factors.\n2. First-line medications include thiazide diuretics, CCBs, and ACE inhibitors or ARBs.\n3. Target BP is typically <130/80 mmHg for most patients.",
                "source": "American College of Cardiology/American Heart Association",
                "year": 2023
            },
            {
                "title": "Heart Failure Management Guidelines",
                "content": "1. Classify patients by ejection fraction: reduced (HFrEF), mildly reduced (HFmrEF), or preserved (HFpEF).\n2. For HFrEF, use GDMT including ACEI/ARB/ARNI, beta-blockers, MRAs, and SGLT2 inhibitors.\n3. Address comorbidities including hypertension, diabetes, and sleep apnea.",
                "source": "American College of Cardiology/American Heart Association",
                "year": 2022
            }
        ]
        
        for guideline_data in guidelines:
            self.add_guideline(
                title=guideline_data["title"],
                organization=guideline_data["source"],
                publication_year=guideline_data["year"],
                summary=guideline_data["content"],
                url=None
            )

if __name__ == "__main__":
    importer = CardiologyDataImporter()
    importer.import_data()
