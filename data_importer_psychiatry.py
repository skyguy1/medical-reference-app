"""
Data importer for psychiatry conditions and medications
"""
from models import db, Condition, Medication, Specialty, Guideline
from data_importer_base import BaseDataImporter

class PsychiatryDataImporter(BaseDataImporter):
    """Importer for psychiatry data"""
    
    def __init__(self):
        """Initialize the psychiatry data importer"""
        super().__init__(
            specialty_name="Psychiatry",
            specialty_description="Psychiatry is the medical specialty devoted to the diagnosis, prevention, and treatment of mental disorders."
        )
        # The specialty is already created or retrieved in the base class constructor
    
    def import_data(self):
        """Import all psychiatry data"""
        self.import_conditions()
        self.import_medications()
        self.import_guidelines()
        return True
    
    def import_conditions(self):
        """Import psychiatry-specific conditions"""
        conditions = []
        
        # Major Depressive Disorder
        depression = self.add_condition(
            name="Major Depressive Disorder",
            description="A mood disorder characterized by persistent feelings of sadness and loss of interest.",
            symptoms=[
                "Persistent sad, anxious, or empty mood",
                "Loss of interest in activities once enjoyed",
                "Decreased energy, fatigue",
                "Difficulty sleeping or oversleeping",
                "Changes in appetite or weight",
                "Thoughts of death or suicide",
                "Difficulty concentrating or making decisions"
            ],
            treatments=[
                "Selective Serotonin Reuptake Inhibitors (SSRIs)",
                "Serotonin-Norepinephrine Reuptake Inhibitors (SNRIs)",
                "Atypical antidepressants",
                "Cognitive Behavioral Therapy (CBT)",
                "Interpersonal therapy",
                "Electroconvulsive therapy (in severe cases)"
            ],
            references=[
                {"title": "American Psychiatric Association: Depression", "url": "https://www.psychiatry.org/patients-families/depression"}
            ]
        )
        conditions.append(depression)
        
        # Generalized Anxiety Disorder
        anxiety = self.add_condition(
            name="Generalized Anxiety Disorder",
            description="A mental health disorder characterized by excessive, persistent worry about everyday events and activities.",
            symptoms=[
                "Excessive worry and anxiety",
                "Restlessness or feeling on edge",
                "Fatigue",
                "Difficulty concentrating",
                "Irritability",
                "Muscle tension",
                "Sleep disturbances"
            ],
            treatments=[
                "Selective Serotonin Reuptake Inhibitors (SSRIs)",
                "Serotonin-Norepinephrine Reuptake Inhibitors (SNRIs)",
                "Benzodiazepines (short-term use)",
                "Buspirone",
                "Cognitive Behavioral Therapy (CBT)",
                "Relaxation techniques"
            ],
            references=[
                {"title": "American Psychiatric Association: Anxiety Disorders", "url": "https://www.psychiatry.org/patients-families/anxiety-disorders"}
            ]
        )
        conditions.append(anxiety)
        
        # Bipolar Disorder
        bipolar = self.add_condition(
            name="Bipolar Disorder",
            description="A mental health condition that causes extreme mood swings including emotional highs (mania or hypomania) and lows (depression).",
            symptoms=[
                "Manic episodes: Elevated mood, increased energy, decreased need for sleep",
                "Depressive episodes: Feelings of sadness, emptiness, hopelessness",
                "Mixed episodes: Features of both mania and depression",
                "Impaired judgment and impulsivity during manic episodes",
                "Suicidal thoughts during depressive episodes"
            ],
            treatments=[
                "Mood stabilizers (lithium, valproate)",
                "Atypical antipsychotics",
                "Antidepressants (with mood stabilizers)",
                "Psychotherapy",
                "Electroconvulsive therapy (in severe cases)"
            ],
            references=[
                {"title": "American Psychiatric Association: Bipolar Disorders", "url": "https://www.psychiatry.org/patients-families/bipolar-disorders"}
            ]
        )
        conditions.append(bipolar)
        
        # Schizophrenia
        schizophrenia = self.add_condition(
            name="Schizophrenia",
            description="A chronic brain disorder that affects how a person thinks, feels, and behaves.",
            symptoms=[
                "Positive symptoms: Hallucinations, delusions, thought disorders",
                "Negative symptoms: Reduced emotional expression, avolition, anhedonia",
                "Cognitive symptoms: Problems with attention, memory, and executive functioning",
                "Disorganized speech and behavior"
            ],
            treatments=[
                "Typical antipsychotics",
                "Atypical antipsychotics",
                "Psychosocial interventions",
                "Cognitive remediation",
                "Family education and support"
            ],
            references=[
                {"title": "American Psychiatric Association: Schizophrenia", "url": "https://www.psychiatry.org/patients-families/schizophrenia"}
            ]
        )
        conditions.append(schizophrenia)
        
        # ADHD
        adhd = self.add_condition(
            name="Attention-Deficit/Hyperactivity Disorder",
            description="A neurodevelopmental disorder characterized by persistent patterns of inattention, hyperactivity, and impulsivity.",
            symptoms=[
                "Inattention: Difficulty sustaining attention, easily distracted",
                "Hyperactivity: Fidgeting, excessive talking, restlessness",
                "Impulsivity: Interrupting others, difficulty waiting turn",
                "Disorganization and forgetfulness",
                "Poor time management"
            ],
            treatments=[
                "Stimulant medications (methylphenidate, amphetamine)",
                "Non-stimulant medications (atomoxetine, guanfacine)",
                "Behavioral therapy",
                "Parent training",
                "Educational interventions"
            ],
            references=[
                {"title": "American Psychiatric Association: ADHD", "url": "https://www.psychiatry.org/patients-families/adhd"}
            ]
        )
        conditions.append(adhd)
        
        print(f"Imported {len(conditions)} psychiatry conditions")
        return conditions
    
    def import_medications(self):
        """Import psychiatry-specific medications"""
        medications = []
        
        # Fluoxetine (Prozac)
        fluoxetine = self.add_medication(
            name="Fluoxetine (Prozac)",
            class_name="Selective Serotonin Reuptake Inhibitor (SSRI)",
            description="Fluoxetine is an antidepressant that works by increasing the levels of serotonin in the brain. It's commonly used to treat depression, OCD, panic attacks, and bulimia.",
            uses=[
                "Major Depressive Disorder",
                "Obsessive-Compulsive Disorder",
                "Panic Disorder",
                "Bulimia Nervosa"
            ],
            side_effects=[
                "Nausea",
                "Insomnia",
                "Headache",
                "Anxiety",
                "Sexual dysfunction",
                "Decreased appetite"
            ],
            dosing="20-80 mg daily, typically starting at 20 mg",
            contraindications=[
                "Use of MAO inhibitors within 14 days",
                "Hypersensitivity to fluoxetine"
            ]
        )
        medications.append(fluoxetine)
        
        # Sertraline (Zoloft)
        sertraline = self.add_medication(
            name="Sertraline (Zoloft)",
            class_name="Selective Serotonin Reuptake Inhibitor (SSRI)",
            description="Sertraline is an antidepressant that works by increasing the levels of serotonin in the brain. It's used to treat depression, anxiety, PTSD, and other mood disorders.",
            uses=[
                "Major Depressive Disorder",
                "Panic Disorder",
                "Post-Traumatic Stress Disorder",
                "Obsessive-Compulsive Disorder",
                "Social Anxiety Disorder"
            ],
            side_effects=[
                "Nausea",
                "Diarrhea",
                "Insomnia",
                "Dizziness",
                "Sexual dysfunction",
                "Tremor"
            ],
            dosing="50-200 mg daily, typically starting at 50 mg",
            contraindications=[
                "Use of MAO inhibitors within 14 days",
                "Concurrent use of pimozide",
                "Hypersensitivity to sertraline"
            ]
        )
        medications.append(sertraline)
        
        # Lithium
        lithium = self.add_medication(
            name="Lithium",
            class_name="Mood Stabilizer",
            description="Lithium is a mood stabilizer that helps reduce the severity and frequency of manic episodes in bipolar disorder. It's one of the oldest and most effective treatments for bipolar disorder.",
            uses=[
                "Bipolar Disorder",
                "Treatment-resistant depression"
            ],
            side_effects=[
                "Tremor",
                "Increased thirst and urination",
                "Nausea",
                "Weight gain",
                "Hypothyroidism",
                "Renal effects",
                "Cognitive dulling"
            ],
            dosing="900-1800 mg daily in divided doses, titrated based on serum levels",
            contraindications=[
                "Significant renal impairment",
                "Severe cardiovascular disease",
                "Dehydration",
                "Sodium depletion"
            ]
        )
        medications.append(lithium)
        
        # Risperidone (Risperdal)
        risperidone = self.add_medication(
            name="Risperidone (Risperdal)",
            class_name="Atypical Antipsychotic",
            description="Risperidone is an atypical antipsychotic medication that works by balancing dopamine and serotonin to improve thinking, mood, and behavior. It's used to treat schizophrenia, bipolar disorder, and irritability in autism.",
            uses=[
                "Schizophrenia",
                "Bipolar Disorder",
                "Irritability associated with autism"
            ],
            side_effects=[
                "Weight gain",
                "Sedation",
                "Extrapyramidal symptoms",
                "Hyperprolactinemia",
                "Metabolic changes",
                "Orthostatic hypotension"
            ],
            dosing="2-8 mg daily for schizophrenia, 1-6 mg daily for bipolar disorder",
            contraindications=[
                "Hypersensitivity to risperidone"
            ]
        )
        medications.append(risperidone)
        
        # Methylphenidate (Ritalin)
        methylphenidate = self.add_medication(
            name="Methylphenidate (Ritalin)",
            class_name="Stimulant",
            description="Methylphenidate is a central nervous system stimulant that affects chemicals in the brain and nerves that contribute to hyperactivity and impulse control. It's primarily used to treat ADHD and narcolepsy.",
            uses=[
                "Attention-Deficit/Hyperactivity Disorder",
                "Narcolepsy"
            ],
            side_effects=[
                "Decreased appetite",
                "Insomnia",
                "Headache",
                "Increased heart rate and blood pressure",
                "Anxiety",
                "Irritability"
            ],
            dosing="20-60 mg daily in divided doses",
            contraindications=[
                "Hypersensitivity to methylphenidate",
                "Glaucoma",
                "Motor tics or Tourette's syndrome",
                "Severe anxiety or agitation",
                "Use of MAO inhibitors within 14 days"
            ]
        )
        medications.append(methylphenidate)
        
        # Link medications to conditions
        self.link_medication_to_condition("Fluoxetine (Prozac)", "Major Depressive Disorder")
        self.link_medication_to_condition("Fluoxetine (Prozac)", "Generalized Anxiety Disorder")
        self.link_medication_to_condition("Sertraline (Zoloft)", "Major Depressive Disorder")
        self.link_medication_to_condition("Sertraline (Zoloft)", "Generalized Anxiety Disorder")
        self.link_medication_to_condition("Lithium", "Bipolar Disorder")
        self.link_medication_to_condition("Risperidone (Risperdal)", "Schizophrenia")
        self.link_medication_to_condition("Risperidone (Risperdal)", "Bipolar Disorder")
        self.link_medication_to_condition("Methylphenidate (Ritalin)", "Attention-Deficit/Hyperactivity Disorder")
        
        print(f"Imported {len(medications)} psychiatry medications")
        return medications
    
    def import_references(self):
        """Import psychiatry-specific references"""
        references = [
            {
                "title": "American Psychiatric Association",
                "url": "https://www.psychiatry.org/",
                "description": "Professional organization of psychiatrists providing resources for mental health."
            },
            {
                "title": "National Institute of Mental Health",
                "url": "https://www.nimh.nih.gov/",
                "description": "Lead federal agency for research on mental disorders."
            },
            {
                "title": "Mental Health America",
                "url": "https://www.mhanational.org/",
                "description": "Community-based nonprofit dedicated to addressing the needs of those living with mental illness."
            }
        ]
        
        for reference_data in references:
            self.add_reference(
                title=reference_data["title"],
                url=reference_data["url"],
                description=reference_data.get("description")
            )
        
        print(f"Imported {len(references)} psychiatry references")
    
    def import_guidelines(self):
        """Import psychiatry-specific guidelines"""
        guidelines = [
            {
                "title": "APA Practice Guideline for the Treatment of Patients with Major Depressive Disorder",
                "organization": "American Psychiatric Association",
                "publication_year": 2022,
                "url": "https://psychiatryonline.org/doi/book/10.1176/appi.books.9780890425787",
                "summary": "Evidence-based recommendations for the assessment and treatment of patients with major depressive disorder."
            },
            {
                "title": "Practice Guideline for the Treatment of Patients with Schizophrenia",
                "organization": "American Psychiatric Association",
                "publication_year": 2021,
                "url": "https://psychiatryonline.org/doi/book/10.1176/appi.books.9780890424841",
                "summary": "Evidence-based recommendations for the treatment of schizophrenia."
            },
            {
                "title": "Clinical Practice Guidelines for the Management of ADHD in Children, Adolescents, and Adults",
                "organization": "American Academy of Pediatrics",
                "publication_year": 2019,
                "url": "https://publications.aap.org/pediatrics/article/144/4/e20192528/81590/Clinical-Practice-Guideline-for-the-Diagnosis",
                "summary": "Guidelines for the evaluation, diagnosis, and treatment of ADHD."
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
        
        print(f"Imported {len(guidelines)} psychiatry guidelines")


if __name__ == "__main__":
    importer = PsychiatryDataImporter()
    importer.import_data()
