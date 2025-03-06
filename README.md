# Medical Reference Application

A comprehensive web-based medical reference application similar to UpToDate, providing evidence-based clinical information for healthcare professionals.

## Features

- Search for medical conditions, treatments, and medications
- Browse medical specialties and topics
- View detailed clinical information with references
- Filter medications by specialty, class, and usage
- User authentication and personalized favorites
- Admin panel for content management
- Responsive design for desktop and mobile use

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```
   python init_db.py
   ```
4. Import medical data:
   ```
   python run_batch_importers.py
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `app.py`: Main Flask application with routes and controllers
- `models.py`: SQLAlchemy database models
- `templates/`: HTML templates for the web interface
- `static/`: Static files (CSS, JavaScript, images)
- `data_importer_*.py`: Specialty-specific data importers
- `import_medications_batch*.py`: Batch medication importers
- `run_batch_importers.py`: Script to run all importers and generate relationships

## Technologies Used

- Backend: Flask (Python), SQLAlchemy
- Frontend: HTML, CSS, JavaScript
- UI Framework: Bootstrap 5
- Database: SQLite (development), PostgreSQL (production-ready)
- Authentication: JWT for API access

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
