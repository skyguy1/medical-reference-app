#!/bin/bash
# exit on error
set -o errexit

# Install dependencies
pip install flask flask-sqlalchemy flask-login werkzeug

# Initialize the database
python -c "from isolated_app import app, db; app.app_context().push(); db.create_all()"

# Import sample data if needed
python -c "
from isolated_app import app, db, Specialty, Medication, Condition, Guideline, User
from datetime import datetime

with app.app_context():
    # Create admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    
    # Create specialties
    if not Specialty.query.first():
        specialties = [
            Specialty(name='Cardiology', description='Deals with disorders of the heart and blood vessels'),
            Specialty(name='Neurology', description='Focuses on disorders of the nervous system'),
            Specialty(name='Pediatrics', description='Medical care of infants, children, and adolescents'),
            Specialty(name='Psychiatry', description='Diagnosis, prevention, and treatment of mental disorders')
        ]
        db.session.add_all(specialties)
        db.session.commit()
    
    # Create medications
    if not Medication.query.first():
        medications = [
            Medication(
                name='Aspirin', 
                generic_name='Acetylsalicylic acid',
                drug_class='NSAID',
                description='Common pain reliever and anti-inflammatory',
                dosage='325-650mg every 4-6 hours',
                side_effects='Stomach upset, heartburn, easy bruising or bleeding',
                contraindications='Bleeding disorders, aspirin allergy, children with viral infections'
            ),
            Medication(
                name='Lisinopril', 
                generic_name='Lisinopril',
                drug_class='ACE Inhibitor',
                description='Used to treat high blood pressure and heart failure',
                dosage='10-40mg once daily',
                side_effects='Dry cough, dizziness, headache, fatigue',
                contraindications='Pregnancy, history of angioedema'
            ),
            Medication(
                name='Prozac', 
                generic_name='Fluoxetine',
                drug_class='SSRI',
                description='Antidepressant used to treat depression, OCD, and panic attacks',
                dosage='20-80mg daily',
                side_effects='Nausea, insomnia, headache, anxiety',
                contraindications='Use with MAOIs, thioridazine'
            )
        ]
        db.session.add_all(medications)
        db.session.commit()
    
    # Create conditions
    if not Condition.query.first():
        conditions = [
            Condition(
                name='Hypertension',
                description='High blood pressure',
                symptoms='Usually asymptomatic, headache, shortness of breath',
                diagnosis='Blood pressure readings consistently above 130/80 mmHg',
                treatment='Lifestyle modifications, medications like ACE inhibitors, diuretics'
            ),
            Condition(
                name='Major Depressive Disorder',
                description='Mood disorder causing persistent feeling of sadness',
                symptoms='Persistent sadness, loss of interest, sleep disturbances',
                diagnosis='Clinical interview, DSM-5 criteria',
                treatment='Psychotherapy, antidepressants, lifestyle changes'
            ),
            Condition(
                name='Migraine',
                description='Recurring headaches of moderate to severe intensity',
                symptoms='Throbbing pain, nausea, sensitivity to light and sound',
                diagnosis='Clinical history, absence of other causes',
                treatment='Pain relievers, preventive medications, lifestyle modifications'
            )
        ]
        db.session.add_all(conditions)
        db.session.commit()
    
    # Create guidelines
    if not Guideline.query.first():
        guidelines = [
            Guideline(
                title='Hypertension Management Guidelines',
                content='Comprehensive approach to managing hypertension...',
                source='American Heart Association',
                publication_date=datetime(2023, 1, 15),
                summary='Guidelines for diagnosis and treatment of hypertension',
                evidence_level='Level A',
                recommendations='Regular monitoring, lifestyle modifications, medication therapy'
            ),
            Guideline(
                title='Depression Treatment Guidelines',
                content='Evidence-based approaches to treating depression...',
                source='American Psychiatric Association',
                publication_date=datetime(2022, 6, 10),
                summary='Guidelines for management of major depressive disorder',
                evidence_level='Level A',
                recommendations='Psychotherapy, pharmacotherapy, combined approaches'
            )
        ]
        db.session.add_all(guidelines)
        db.session.commit()
    
    # Create associations
    cardiology = Specialty.query.filter_by(name='Cardiology').first()
    psychiatry = Specialty.query.filter_by(name='Psychiatry').first()
    neurology = Specialty.query.filter_by(name='Neurology').first()
    
    hypertension = Condition.query.filter_by(name='Hypertension').first()
    depression = Condition.query.filter_by(name='Major Depressive Disorder').first()
    migraine = Condition.query.filter_by(name='Migraine').first()
    
    lisinopril = Medication.query.filter_by(name='Lisinopril').first()
    prozac = Medication.query.filter_by(name='Prozac').first()
    aspirin = Medication.query.filter_by(name='Aspirin').first()
    
    hyp_guideline = Guideline.query.filter_by(title='Hypertension Management Guidelines').first()
    dep_guideline = Guideline.query.filter_by(title='Depression Treatment Guidelines').first()
    
    # Associate specialties with conditions
    if cardiology and hypertension:
        cardiology.conditions.append(hypertension)
    if psychiatry and depression:
        psychiatry.conditions.append(depression)
    if neurology and migraine:
        neurology.conditions.append(migraine)
    
    # Associate medications with conditions
    if lisinopril and hypertension:
        lisinopril.conditions.append(hypertension)
    if prozac and depression:
        prozac.conditions.append(depression)
    if aspirin and migraine:
        aspirin.conditions.append(migraine)
    
    # Associate guidelines with specialties and conditions
    if hyp_guideline:
        if cardiology:
            hyp_guideline.specialties.append(cardiology)
        if hypertension:
            hyp_guideline.conditions.append(hypertension)
    
    if dep_guideline:
        if psychiatry:
            dep_guideline.specialties.append(psychiatry)
        if depression:
            dep_guideline.conditions.append(depression)
    
    db.session.commit()
"
