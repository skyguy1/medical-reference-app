#!/bin/bash
# exit on error
set -o errexit

# Install dependencies
pip install -r standalone/requirements.txt

# Initialize the database
python -c "from standalone.app import app, db; app.app_context().push(); db.create_all()"

# Import sample data if needed
python -c "
from standalone.app import app, db
from standalone.import_data import import_specialties, import_medications, import_conditions, import_guidelines

with app.app_context():
    import_specialties()
    import_medications()
    import_conditions()
    import_guidelines()
"
