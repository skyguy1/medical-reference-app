"""
Data import script for the Medical Reference App
"""
from app import app, db, Medication, Condition

def import_sample_data():
    """Import sample medications and conditions into the database"""
    print("Importing sample data...")
    
    # Clear existing data
    db.session.query(Medication).delete()
    db.session.query(Condition).delete()
    db.session.commit()
    
    # Sample medications
    medications = [
        {
            'name': 'Aspirin',
            'description': 'Aspirin is a nonsteroidal anti-inflammatory drug (NSAID) used to reduce pain, fever, and inflammation.',
            'dosage': 'Adults: 325-650 mg every 4-6 hours as needed. Maximum 4g daily.',
            'side_effects': 'Stomach upset, heartburn, stomach/intestinal bleeding, allergic reactions.',
            'contraindications': 'Allergy to NSAIDs, bleeding disorders, children with viral infections (risk of Reye syndrome).'
        },
        {
            'name': 'Lisinopril',
            'description': 'Lisinopril is an ACE inhibitor used to treat high blood pressure and heart failure.',
            'dosage': 'Hypertension: Initial 10mg once daily, maintenance 20-40mg once daily.',
            'side_effects': 'Dry cough, dizziness, headache, fatigue, hypotension.',
            'contraindications': 'Pregnancy, history of angioedema, bilateral renal artery stenosis.'
        },
        {
            'name': 'Metformin',
            'description': 'Metformin is a biguanide antihyperglycemic agent used for treating type 2 diabetes.',
            'dosage': 'Initial: 500mg twice daily or 850mg once daily. Maximum: 2550mg/day in divided doses.',
            'side_effects': 'Diarrhea, nausea, vomiting, flatulence, lactic acidosis (rare but serious).',
            'contraindications': 'Renal dysfunction, acute or chronic metabolic acidosis, hypersensitivity.'
        },
        {
            'name': 'Atorvastatin',
            'description': 'Atorvastatin is a statin medication used to prevent cardiovascular disease and treat abnormal lipid levels.',
            'dosage': 'Initial: 10-20mg once daily. Maintenance: 10-80mg once daily.',
            'side_effects': 'Muscle pain, liver enzyme elevation, headache, joint pain.',
            'contraindications': 'Active liver disease, pregnancy, breastfeeding.'
        },
        {
            'name': 'Levothyroxine',
            'description': 'Levothyroxine is a synthetic thyroid hormone used to treat hypothyroidism.',
            'dosage': 'Adults: Initial 25-50mcg daily, adjusted by 25-50mcg increments every 4-6 weeks.',
            'side_effects': 'Headache, insomnia, nervousness, fever, weight loss, chest pain (with overdose).',
            'contraindications': 'Thyrotoxicosis, acute myocardial infarction, uncorrected adrenal insufficiency.'
        }
    ]
    
    # Sample conditions
    conditions = [
        {
            'name': 'Hypertension',
            'description': 'Hypertension, or high blood pressure, is a condition in which the force of blood against the artery walls is too high.',
            'symptoms': 'Often asymptomatic. May include headaches, shortness of breath, nosebleeds in severe cases.',
            'treatments': 'Lifestyle modifications (diet, exercise, weight loss), medications (ACE inhibitors, ARBs, diuretics, calcium channel blockers).'
        },
        {
            'name': 'Type 2 Diabetes',
            'description': 'Type 2 diabetes is a chronic condition that affects the way the body metabolizes sugar (glucose).',
            'symptoms': 'Increased thirst, frequent urination, hunger, fatigue, blurred vision, slow-healing sores.',
            'treatments': 'Lifestyle modifications, oral medications (metformin, sulfonylureas, DPP-4 inhibitors), insulin therapy.'
        },
        {
            'name': 'Coronary Artery Disease',
            'description': 'Coronary artery disease is the narrowing or blockage of the coronary arteries, usually caused by atherosclerosis.',
            'symptoms': 'Chest pain (angina), shortness of breath, fatigue, heart attack.',
            'treatments': 'Lifestyle changes, medications (statins, aspirin, beta-blockers), procedures (angioplasty, stent placement, bypass surgery).'
        },
        {
            'name': 'Hypothyroidism',
            'description': 'Hypothyroidism is a condition in which the thyroid gland doesn\'t produce enough thyroid hormone.',
            'symptoms': 'Fatigue, increased sensitivity to cold, constipation, dry skin, weight gain, puffy face, hoarseness, muscle weakness.',
            'treatments': 'Thyroid hormone replacement therapy (levothyroxine).'
        },
        {
            'name': 'Asthma',
            'description': 'Asthma is a condition in which airways narrow and swell and may produce extra mucus, making breathing difficult.',
            'symptoms': 'Shortness of breath, chest tightness or pain, wheezing, trouble sleeping due to breathing problems.',
            'treatments': 'Quick-relief medications (bronchodilators), long-term control medications (inhaled corticosteroids, leukotriene modifiers).'
        }
    ]
    
    # Add medications to database
    for med_data in medications:
        medication = Medication(**med_data)
        db.session.add(medication)
    
    # Add conditions to database
    for cond_data in conditions:
        condition = Condition(**cond_data)
        db.session.add(condition)
    
    # Commit changes
    db.session.commit()
    print("Sample data imported successfully!")

if __name__ == '__main__':
    with app.app_context():
        import_sample_data()
