from app import app
from models import db, Medication

with app.app_context():
    medications = Medication.query.all()
    print(f"Total medications: {len(medications)}")
    print("\nFirst 10 medications:")
    for med in medications[:10]:
        print(f"ID: {med.id}, Name: {med.name}")
    
    # Check for specific medications
    lisinopril = Medication.query.filter(Medication.name.like('%Lisinopril%')).all()
    print(f"\nLisinopril medications: {len(lisinopril)}")
    for med in lisinopril:
        print(f"ID: {med.id}, Name: {med.name}")
    
    levetiracetam = Medication.query.filter(Medication.name.like('%Levetiracetam%')).all()
    print(f"\nLevetiracetam medications: {len(levetiracetam)}")
    for med in levetiracetam:
        print(f"ID: {med.id}, Name: {med.name}")
    
    isotretinoin = Medication.query.filter(Medication.name.like('%Isotretinoin%')).all()
    print(f"\nIsotretinoin medications: {len(isotretinoin)}")
    for med in isotretinoin:
        print(f"ID: {med.id}, Name: {med.name}")
