"""
Gastroenterology Data Importer

This module imports gastroenterology-related conditions and medications
into the medical reference database.
"""
from data_importer_base import BaseDataImporter

class GIDataImporter(BaseDataImporter):
    """
    Importer for gastroenterology-related medical data
    """
    
    def __init__(self):
        """Initialize the GI data importer with specialty information"""
        super().__init__(
            specialty_name="Gastroenterology",
            specialty_description="Branch of medicine focused on the digestive system and its disorders."
        )
    
    def import_data(self):
        """Import all gastroenterology data"""
        self.import_conditions()
        self.import_medications()
        return True
    
    def import_conditions(self):
        """Import gastroenterology-specific conditions"""
        conditions = []
        
        # GERD
        gerd = self.add_condition(
            name="Gastroesophageal Reflux Disease (GERD)",
            description="Gastroesophageal reflux disease (GERD) occurs when stomach acid frequently flows back into the tube connecting your mouth and stomach (esophagus). This backwash (acid reflux) can irritate the lining of your esophagus.",
            symptoms=[
                "Heartburn", 
                "Regurgitation of food or sour liquid", 
                "Difficulty swallowing", 
                "Sensation of a lump in your throat", 
                "Chronic cough", 
                "Laryngitis", 
                "New or worsening asthma", 
                "Disrupted sleep"
            ],
            treatments=[
                "Lifestyle modifications", 
                "Over-the-counter antacids", 
                "H2 receptor blockers", 
                "Proton pump inhibitors", 
                "Surgery in severe cases"
            ],
            references=[
                {"title": "American College of Gastroenterology Guidelines, 2023", "url": "https://gi.org/"},
                {"title": "American Gastroenterological Association, 2022", "url": "https://gastro.org/"}
            ]
        )
        conditions.append(gerd)
        
        # Peptic Ulcer Disease
        pud = self.add_condition(
            name="Peptic Ulcer Disease",
            description="Peptic ulcers are open sores that develop on the inside lining of your stomach and the upper portion of your small intestine. The most common cause is infection with the bacterium Helicobacter pylori (H. pylori).",
            symptoms=[
                "Burning stomach pain", 
                "Feeling of fullness, bloating or belching", 
                "Fatty food intolerance", 
                "Heartburn", 
                "Nausea"
            ],
            treatments=[
                "Antibiotics to kill H. pylori", 
                "Proton pump inhibitors", 
                "H2 receptor blockers", 
                "Antacids", 
                "Cytoprotective agents"
            ],
            references=[
                {"title": "American College of Gastroenterology Guidelines, 2023", "url": "https://gi.org/"},
                {"title": "World Gastroenterology Organisation, 2022", "url": "https://www.worldgastroenterology.org/"}
            ]
        )
        conditions.append(pud)
        
        # Inflammatory Bowel Disease (IBD)
        ibd = self.add_condition(
            name="Inflammatory Bowel Disease (IBD)",
            description="Inflammatory bowel disease (IBD) involves chronic inflammation of all or part of your digestive tract. IBD primarily includes ulcerative colitis and Crohn's disease.",
            symptoms=[
                "Diarrhea", 
                "Fatigue", 
                "Abdominal pain and cramping", 
                "Blood in stool", 
                "Reduced appetite", 
                "Unintended weight loss", 
                "Fever", 
                "Joint pain"
            ],
            treatments=[
                "Anti-inflammatory drugs", 
                "Immunosuppressants", 
                "Biologics", 
                "Antibiotics", 
                "Nutritional therapy", 
                "Surgery"
            ],
            references=[
                {"title": "American College of Gastroenterology Guidelines, 2023", "url": "https://gi.org/"},
                {"title": "Crohn's and Colitis Foundation, 2022", "url": "https://www.crohnscolitisfoundation.org/"}
            ]
        )
        conditions.append(ibd)
        
        # Irritable Bowel Syndrome (IBS)
        ibs = self.add_condition(
            name="Irritable Bowel Syndrome (IBS)",
            description="Irritable bowel syndrome (IBS) is a common disorder that affects the large intestine. Signs and symptoms include cramping, abdominal pain, bloating, gas, and diarrhea or constipation, or both.",
            symptoms=[
                "Abdominal pain, cramping or bloating", 
                "Excess gas", 
                "Diarrhea or constipation, sometimes alternating", 
                "Mucus in the stool", 
                "Changes in appearance of bowel movements", 
                "Changes in how often you have bowel movements"
            ],
            treatments=[
                "Dietary changes (low FODMAP diet)", 
                "Fiber supplements", 
                "Anti-diarrheal medications", 
                "Antispasmodic agents", 
                "Antidepressants", 
                "Cognitive behavioral therapy"
            ],
            references=[
                {"title": "American College of Gastroenterology Guidelines, 2023", "url": "https://gi.org/"},
                {"title": "International Foundation for Gastrointestinal Disorders, 2022", "url": "https://aboutibs.org/"}
            ]
        )
        conditions.append(ibs)
        
        # Celiac Disease
        celiac = self.add_condition(
            name="Celiac Disease",
            description="Celiac disease is an immune reaction to eating gluten, a protein found in wheat, barley, and rye. Over time, this reaction damages the lining of the small intestine and prevents absorption of nutrients.",
            symptoms=[
                "Diarrhea", 
                "Fatigue", 
                "Weight loss", 
                "Bloating and gas", 
                "Abdominal pain", 
                "Nausea and vomiting", 
                "Constipation", 
                "Dermatitis herpetiformis (itchy skin rash)"
            ],
            treatments=[
                "Strict gluten-free diet", 
                "Nutritional supplements", 
                "Medication to control intestinal inflammation", 
                "Dermatitis herpetiformis medications"
            ],
            references=[
                {"title": "American College of Gastroenterology Guidelines, 2023", "url": "https://gi.org/"},
                {"title": "Celiac Disease Foundation, 2022", "url": "https://celiac.org/"}
            ]
        )
        conditions.append(celiac)
        
        # Hepatitis
        hepatitis = self.add_condition(
            name="Hepatitis",
            description="Hepatitis is an inflammation of the liver. The condition can be self-limiting or can progress to fibrosis (scarring), cirrhosis or liver cancer. Hepatitis viruses are the most common cause of hepatitis in the world but other infections, toxic substances, and autoimmune diseases can also cause hepatitis.",
            symptoms=[
                "Fatigue", 
                "Flu-like symptoms", 
                "Dark urine", 
                "Pale stool", 
                "Abdominal pain", 
                "Loss of appetite", 
                "Weight loss", 
                "Jaundice"
            ],
            treatments=[
                "Rest", 
                "Adequate nutrition and fluids", 
                "Antiviral medications", 
                "Liver transplant in severe cases"
            ],
            references=[
                {"title": "American Association for the Study of Liver Diseases, 2023", "url": "https://aasld.org/"},
                {"title": "World Health Organization, 2022", "url": "https://www.who.int/"}
            ]
        )
        conditions.append(hepatitis)
        
        print(f"Imported {len(conditions)} gastroenterology conditions")
        return conditions
    
    def import_medications(self):
        """Import gastroenterology-specific medications"""
        medications = []
        
        # Omeprazole
        omeprazole = self.add_medication(
            name="Omeprazole",
            class_name="Proton pump inhibitor",
            description="Omeprazole is a proton pump inhibitor that decreases stomach acid production. It's commonly used to treat gastroesophageal reflux disease (GERD), peptic ulcer disease, and as part of combination therapy for H. pylori infection.",
            uses=[
                "GERD", 
                "Peptic ulcer disease", 
                "H. pylori infection (as part of combination therapy)", 
                "Zollinger-Ellison syndrome"
            ],
            side_effects=[
                "Headache", 
                "Abdominal pain", 
                "Diarrhea", 
                "Nausea", 
                "Vitamin B12 deficiency (long-term use)", 
                "Increased risk of bone fractures (long-term use)"
            ],
            dosing="20-40 mg once daily",
            contraindications=[
                "Hypersensitivity to omeprazole or other proton pump inhibitors"
            ]
        )
        medications.append(omeprazole)
        
        # Mesalamine
        mesalamine = self.add_medication(
            name="Mesalamine",
            class_name="5-Aminosalicylic acid (5-ASA)",
            description="Mesalamine is an anti-inflammatory drug that acts locally in the gut to reduce inflammation. It's primarily used to treat ulcerative colitis and Crohn's disease, helping to induce and maintain remission.",
            uses=[
                "Ulcerative colitis", 
                "Crohn's disease"
            ],
            side_effects=[
                "Headache", 
                "Abdominal pain", 
                "Nausea", 
                "Diarrhea", 
                "Rash", 
                "Nephrotoxicity (rare)"
            ],
            dosing="2-4.8 g daily in divided doses",
            contraindications=[
                "Hypersensitivity to mesalamine, salicylates, or any component of the formulation", 
                "Severe renal impairment"
            ]
        )
        medications.append(mesalamine)
        
        # Infliximab
        infliximab = self.add_medication(
            name="Infliximab",
            class_name="Tumor necrosis factor (TNF) inhibitor",
            description="Infliximab is a biologic medication that blocks the action of tumor necrosis factor-alpha (TNF-alpha), a protein that promotes inflammation in the body. It's used to treat various inflammatory conditions, including Crohn's disease, ulcerative colitis, rheumatoid arthritis, ankylosing spondylitis, psoriatic arthritis, and plaque psoriasis.",
            uses=[
                "Crohn's disease", 
                "Ulcerative colitis", 
                "Rheumatoid arthritis", 
                "Ankylosing spondylitis", 
                "Psoriatic arthritis", 
                "Plaque psoriasis"
            ],
            side_effects=[
                "Infusion reactions", 
                "Increased risk of infections", 
                "Reactivation of tuberculosis", 
                "Hepatotoxicity", 
                "Demyelinating disorders", 
                "Lupus-like syndrome", 
                "Increased risk of certain cancers"
            ],
            dosing="5 mg/kg IV at 0, 2, and 6 weeks, then every 8 weeks",
            contraindications=[
                "Hypersensitivity to infliximab", 
                "Moderate to severe heart failure (NYHA Class III/IV)", 
                "Active tuberculosis or other severe infections"
            ]
        )
        medications.append(infliximab)
        
        # Rifaximin
        rifaximin = self.add_medication(
            name="Rifaximin",
            class_name="Non-systemic antibiotic",
            description="Rifaximin is a non-systemic antibiotic that works by killing bacteria in the gut. It's used to treat traveler's diarrhea, irritable bowel syndrome with diarrhea (IBS-D), and hepatic encephalopathy.",
            uses=[
                "Traveler's diarrhea", 
                "Irritable bowel syndrome with diarrhea (IBS-D)", 
                "Hepatic encephalopathy"
            ],
            side_effects=[
                "Nausea", 
                "Flatulence", 
                "Headache", 
                "Abdominal pain", 
                "Rectal tenesmus", 
                "Defecation urgency"
            ],
            dosing="550 mg three times daily for hepatic encephalopathy; 200 mg three times daily for IBS-D",
            contraindications=[
                "Hypersensitivity to rifaximin, rifamycin antimicrobial agents, or any component of the formulation"
            ]
        )
        medications.append(rifaximin)
        
        # Linaclotide
        linaclotide = self.add_medication(
            name="Linaclotide",
            class_name="Guanylate cyclase-C agonist",
            description="Linaclotide is a guanylate cyclase-C agonist that works by increasing intestinal fluid secretion and promoting bowel movements. It's used to treat irritable bowel syndrome with constipation (IBS-C) and chronic idiopathic constipation (CIC).",
            uses=[
                "Irritable bowel syndrome with constipation (IBS-C)", 
                "Chronic idiopathic constipation (CIC)"
            ],
            side_effects=[
                "Diarrhea", 
                "Abdominal pain", 
                "Flatulence", 
                "Headache", 
                "Abdominal distension"
            ],
            dosing="290 mcg once daily for IBS-C; 145 mcg once daily for CIC",
            contraindications=[
                "Known or suspected mechanical gastrointestinal obstruction", 
                "Patients less than 6 years of age (risk of serious dehydration)"
            ]
        )
        medications.append(linaclotide)
        
        # Dicyclomine
        dicyclomine = self.add_medication(
            name="Dicyclomine",
            class_name="Anticholinergic",
            description="Dicyclomine is an anticholinergic medication that works by relaxing the muscles in the stomach and intestines. It's used to treat irritable bowel syndrome (IBS).",
            uses=[
                "Irritable bowel syndrome"
            ],
            side_effects=[
                "Dry mouth", 
                "Blurred vision", 
                "Constipation", 
                "Urinary retention", 
                "Dizziness"
            ],
            dosing="20-40 mg orally four times daily",
            contraindications=[
                "Glaucoma", 
                "Myasthenia gravis", 
                "Intestinal obstruction", 
                "Severe ulcerative colitis", 
                "Reflux esophagitis"
            ]
        )
        medications.append(dicyclomine)
        
        # Entecavir
        entecavir = self.add_medication(
            name="Entecavir",
            class_name="Antiviral (nucleoside analog)",
            description="Entecavir is an antiviral medication that works by inhibiting the replication of hepatitis B virus. It's used to treat chronic hepatitis B.",
            uses=[
                "Chronic hepatitis B"
            ],
            side_effects=[
                "Headache", 
                "Fatigue", 
                "Dizziness", 
                "Nausea", 
                "Lactic acidosis (rare)"
            ],
            dosing="0.5-1 mg once daily",
            contraindications=[
                "Hypersensitivity to entecavir"
            ]
        )
        medications.append(entecavir)
        
        # Link medications to conditions
        # Omeprazole
        self.link_medication_to_condition("Omeprazole", "Gastroesophageal Reflux Disease (GERD)")
        self.link_medication_to_condition("Omeprazole", "Peptic Ulcer Disease")
        
        # Mesalamine
        self.link_medication_to_condition("Mesalamine", "Inflammatory Bowel Disease")
        
        # Infliximab
        self.link_medication_to_condition("Infliximab", "Inflammatory Bowel Disease")
        
        # Rifaximin
        self.link_medication_to_condition("Rifaximin", "Irritable Bowel Syndrome")
        
        # Linaclotide
        self.link_medication_to_condition("Linaclotide", "Irritable Bowel Syndrome")
        
        # Dicyclomine
        self.link_medication_to_condition("Dicyclomine", "Irritable Bowel Syndrome")
        
        # Entecavir
        self.link_medication_to_condition("Entecavir", "Hepatitis")
        
        print(f"Imported {len(medications)} gastroenterology medications")
        return medications

if __name__ == "__main__":
    importer = GIDataImporter()
    importer.import_data()
