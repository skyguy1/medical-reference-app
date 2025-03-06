"""
Neurology Data Importer

This module imports neurology-related conditions and medications
into the medical reference database.
"""
from data_importer_base import BaseDataImporter

class NeurologyDataImporter(BaseDataImporter):
    """
    Importer for neurology-related medical data
    """
    
    def __init__(self):
        """Initialize the neurology data importer with specialty information"""
        super().__init__(
            specialty_name="Neurology",
            specialty_description="Branch of medicine dealing with disorders of the nervous system."
        )
    
    def import_data(self):
        """Import all neurology data"""
        self.import_conditions()
        self.import_medications()
        return True
    
    def import_conditions(self):
        """Import neurology-specific conditions"""
        conditions = []
        
        # Migraine
        migraine = self.add_condition(
            name="Migraine",
            description="A migraine is a headache that can cause severe throbbing pain or a pulsing sensation, usually on one side of the head. It's often accompanied by nausea, vomiting, and extreme sensitivity to light and sound.",
            symptoms=[
                "Throbbing or pulsating pain", 
                "Light sensitivity", 
                "Sound sensitivity", 
                "Nausea", 
                "Vomiting", 
                "Vision changes or blurred vision", 
                "Aura (visual disturbances)", 
                "Lightheadedness"
            ],
            treatments=[
                "Pain-relieving medications", 
                "Preventive medications", 
                "Lifestyle changes", 
                "Biofeedback", 
                "Acupuncture", 
                "Botox injections"
            ],
            references=[
                {"title": "American Headache Society Guidelines, 2023", "url": "https://americanheadachesociety.org/"},
                {"title": "International Headache Society, 2022", "url": "https://ihs-headache.org/"}
            ]
        )
        conditions.append(migraine)
        
        # Epilepsy
        epilepsy = self.add_condition(
            name="Epilepsy",
            description="Epilepsy is a central nervous system (neurological) disorder in which brain activity becomes abnormal, causing seizures or periods of unusual behavior, sensations, and sometimes loss of awareness.",
            symptoms=[
                "Temporary confusion", 
                "Staring spells", 
                "Uncontrollable jerking movements", 
                "Loss of consciousness or awareness", 
                "Psychic symptoms (fear, anxiety, déjà vu)"
            ],
            treatments=[
                "Anti-seizure medications", 
                "Surgery", 
                "Vagus nerve stimulation", 
                "Ketogenic diet", 
                "Deep brain stimulation"
            ],
            references=[
                {"title": "American Epilepsy Society Guidelines, 2023", "url": "https://www.aesnet.org/"},
                {"title": "International League Against Epilepsy, 2022", "url": "https://www.ilae.org/"}
            ]
        )
        conditions.append(epilepsy)
        
        # Multiple Sclerosis
        ms = self.add_condition(
            name="Multiple Sclerosis",
            description="Multiple sclerosis (MS) is a potentially disabling disease of the brain and spinal cord (central nervous system) in which the immune system attacks the protective sheath (myelin) that covers nerve fibers.",
            symptoms=[
                "Numbness or weakness in limbs", 
                "Electric-shock sensations with certain neck movements", 
                "Tremor", 
                "Lack of coordination", 
                "Vision problems", 
                "Slurred speech", 
                "Fatigue", 
                "Dizziness"
            ],
            treatments=[
                "Disease-modifying therapies", 
                "Corticosteroids", 
                "Plasma exchange", 
                "Physical therapy", 
                "Muscle relaxants", 
                "Medications to reduce fatigue"
            ],
            references=[
                {"title": "National Multiple Sclerosis Society Guidelines, 2023", "url": "https://www.nationalmssociety.org/"},
                {"title": "American Academy of Neurology MS Guidelines, 2022", "url": "https://www.aan.com/"}
            ]
        )
        conditions.append(ms)
        
        # Parkinson's Disease
        parkinsons = self.add_condition(
            name="Parkinson's Disease",
            description="Parkinson's disease is a progressive nervous system disorder that affects movement. Symptoms start gradually, sometimes with a barely noticeable tremor in just one hand.",
            symptoms=[
                "Tremor", 
                "Bradykinesia (slowed movement)", 
                "Rigid muscles", 
                "Impaired posture and balance", 
                "Loss of automatic movements", 
                "Speech changes", 
                "Writing changes"
            ],
            treatments=[
                "Medications to increase dopamine", 
                "MAO B inhibitors", 
                "Catechol O-methyltransferase (COMT) inhibitors", 
                "Deep brain stimulation", 
                "Physical therapy", 
                "Occupational therapy"
            ],
            references=[
                {"title": "American Parkinson Disease Association, 2023", "url": "https://www.apdaparkinson.org/"},
                {"title": "Parkinson's Foundation, 2022", "url": "https://www.parkinson.org/"}
            ]
        )
        conditions.append(parkinsons)
        
        # Alzheimer's Disease
        alzheimers = self.add_condition(
            name="Alzheimer's Disease",
            description="Alzheimer's disease is a progressive disorder that causes brain cells to waste away (degenerate) and die. Alzheimer's disease is the most common cause of dementia — a continuous decline in thinking, behavioral and social skills that disrupts a person's ability to function independently.",
            symptoms=[
                "Memory loss", 
                "Difficulty thinking and reasoning", 
                "Making judgments and decisions", 
                "Planning and performing familiar tasks", 
                "Changes in personality and behavior", 
                "Paranoia and delusions", 
                "Impulsive behavior"
            ],
            treatments=[
                "Cholinesterase inhibitors", 
                "Memantine", 
                "Medications for behavioral symptoms", 
                "Lifestyle modifications", 
                "Cognitive training"
            ],
            references=[
                {"title": "Alzheimer's Association Guidelines, 2023", "url": "https://www.alz.org/"},
                {"title": "National Institute on Aging, 2022", "url": "https://www.nia.nih.gov/"}
            ]
        )
        conditions.append(alzheimers)
        
        # Stroke
        stroke = self.add_condition(
            name="Stroke",
            description="A stroke occurs when the blood supply to part of your brain is interrupted or reduced, preventing brain tissue from getting oxygen and nutrients. Brain cells begin to die in minutes. A stroke is a medical emergency, and prompt treatment is crucial.",
            symptoms=[
                "Trouble speaking and understanding", 
                "Paralysis or numbness of the face, arm or leg", 
                "Problems seeing in one or both eyes", 
                "Headache", 
                "Trouble walking"
            ],
            treatments=[
                "Emergency IV medication", 
                "Emergency endovascular procedures", 
                "Carotid endarterectomy", 
                "Medications to prevent blood clots", 
                "Rehabilitation"
            ],
            references=[
                {"title": "American Stroke Association Guidelines, 2023", "url": "https://www.stroke.org/"},
                {"title": "World Stroke Organization, 2022", "url": "https://www.world-stroke.org/"}
            ]
        )
        conditions.append(stroke)
        
        print(f"Imported {len(conditions)} neurology conditions")
        return conditions
    
    def import_medications(self):
        """Import neurology-specific medications"""
        medications = []
        
        # Sumatriptan
        sumatriptan = self.add_medication(
            name="Sumatriptan",
            class_name="Triptan (serotonin receptor agonist)",
            description="Sumatriptan is a selective serotonin receptor agonist used to treat migraine headaches and cluster headaches. It works by narrowing blood vessels in the brain and reducing the transmission of pain signals.",
            uses=[
                "Migraine", 
                "Cluster headaches"
            ],
            side_effects=[
                "Tingling", 
                "Flushing", 
                "Dizziness", 
                "Drowsiness", 
                "Chest tightness"
            ],
            dosing="25-100 mg orally as needed; 6 mg subcutaneously; 5-20 mg intranasally",
            contraindications=[
                "Ischemic heart disease", 
                "Uncontrolled hypertension", 
                "Hemiplegic or basilar migraine", 
                "Use of MAO inhibitors within 14 days"
            ]
        )
        medications.append(sumatriptan)
        
        # Levetiracetam
        levetiracetam = self.add_medication(
            name="Levetiracetam",
            class_name="Antiepileptic drug",
            description="Levetiracetam is an antiepileptic medication used to treat various types of seizures. It works by stabilizing electrical activity in the brain and preventing seizure activity.",
            uses=[
                "Epilepsy", 
                "Partial onset seizures", 
                "Myoclonic seizures", 
                "Primary generalized tonic-clonic seizures"
            ],
            side_effects=[
                "Somnolence", 
                "Fatigue", 
                "Dizziness", 
                "Behavioral abnormalities", 
                "Coordination difficulties"
            ],
            dosing="500-3000 mg daily in two divided doses",
            contraindications=[
                "Hypersensitivity to levetiracetam"
            ]
        )
        medications.append(levetiracetam)
        
        # Interferon beta-1a
        interferon = self.add_medication(
            name="Interferon beta-1a",
            class_name="Immunomodulator",
            description="Interferon beta-1a is an immunomodulatory medication used to treat multiple sclerosis. It works by reducing inflammation and modulating the immune system's response to the disease.",
            uses=[
                "Multiple Sclerosis"
            ],
            side_effects=[
                "Flu-like symptoms", 
                "Injection site reactions", 
                "Depression", 
                "Elevated liver enzymes", 
                "Blood cell abnormalities"
            ],
            dosing="30 mcg IM once weekly or 44 mcg subcutaneously three times weekly",
            contraindications=[
                "Hypersensitivity to natural or recombinant interferon beta", 
                "Pregnancy category C"
            ]
        )
        medications.append(interferon)
        
        # Carbidopa-Levodopa
        carbidopa_levodopa = self.add_medication(
            name="Carbidopa-Levodopa",
            class_name="Dopamine precursor",
            description="Carbidopa-levodopa is a combination medication used to treat Parkinson's disease. It works by increasing dopamine levels in the brain, which helps to alleviate symptoms of the disease.",
            uses=[
                "Parkinson's Disease", 
                "Parkinsonism"
            ],
            side_effects=[
                "Nausea", 
                "Dizziness", 
                "Headache", 
                "Dyskinesia", 
                "Orthostatic hypotension", 
                "Confusion"
            ],
            dosing="25-100 mg carbidopa/100-400 mg levodopa daily in divided doses",
            contraindications=[
                "Narrow-angle glaucoma", 
                "Melanoma", 
                "Use of nonselective MAO inhibitors"
            ]
        )
        medications.append(carbidopa_levodopa)
        
        # Donepezil
        donepezil = self.add_medication(
            name="Donepezil",
            class_name="Acetylcholinesterase inhibitor",
            description="Donepezil is an acetylcholinesterase inhibitor used to treat Alzheimer's disease. It works by increasing acetylcholine levels in the brain, which helps to improve cognitive function and alleviate symptoms of the disease.",
            uses=[
                "Alzheimer's Disease", 
                "Dementia"
            ],
            side_effects=[
                "Nausea", 
                "Diarrhea", 
                "Insomnia", 
                "Muscle cramps", 
                "Fatigue", 
                "Decreased appetite"
            ],
            dosing="5-10 mg once daily at bedtime",
            contraindications=[
                "Hypersensitivity to donepezil or piperidine derivatives"
            ]
        )
        medications.append(donepezil)
        
        # Alteplase
        alteplase = self.add_medication(
            name="Alteplase",
            class_name="Tissue plasminogen activator (tPA)",
            description="Alteplase is a tissue plasminogen activator used to treat acute ischemic stroke. It works by dissolving blood clots and restoring blood flow to the affected area of the brain.",
            uses=[
                "Ischemic Stroke", 
                "Pulmonary embolism", 
                "Myocardial infarction"
            ],
            side_effects=[
                "Bleeding", 
                "Angioedema", 
                "Nausea", 
                "Hypotension", 
                "Fever"
            ],
            dosing="0.9 mg/kg (maximum 90 mg) IV, with 10% given as bolus over 1 minute and remainder over 60 minutes",
            contraindications=[
                "Active internal bleeding", 
                "Recent intracranial surgery", 
                "Intracranial neoplasm", 
                "Arteriovenous malformation or aneurysm"
            ]
        )
        medications.append(alteplase)
        
        print(f"Imported {len(medications)} neurology medications")
        return medications

if __name__ == "__main__":
    importer = NeurologyDataImporter()
    importer.import_data()
