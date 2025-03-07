"""
Search module for Medical Reference App (without pandas dependency)
"""
from flask import Blueprint, render_template_string, request, session
from sqlalchemy import or_
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
search_bp = Blueprint('search', __name__)

# Search template
SEARCH_TEMPLATE = """
<h2>Search Medical Database</h2>
<div class="card">
    <form method="GET" action="{{ url_for('search.search_results') }}">
        <div style="margin-bottom: 15px;">
            <label for="query">Search Query:</label>
            <input type="text" id="query" name="query" value="{{ query }}" required style="width: 100%; padding: 8px; margin-top: 5px;">
        </div>
        
        <div style="margin-bottom: 15px;">
            <label>Search In:</label>
            <div style="margin-top: 5px;">
                <label style="margin-right: 15px;">
                    <input type="checkbox" name="search_in" value="conditions" checked> Conditions
                </label>
                <label style="margin-right: 15px;">
                    <input type="checkbox" name="search_in" value="medications" checked> Medications
                </label>
                <label style="margin-right: 15px;">
                    <input type="checkbox" name="search_in" value="specialties" checked> Specialties
                </label>
                <label style="margin-right: 15px;">
                    <input type="checkbox" name="search_in" value="references" checked> References
                </label>
                <label>
                    <input type="checkbox" name="search_in" value="guidelines" checked> Guidelines
                </label>
            </div>
        </div>
        
        <button type="submit" class="button">Search</button>
    </form>
</div>

{% if results %}
<h2>Search Results</h2>
<div class="card">
    <p>Found {{ total_results }} results for "{{ query }}"</p>
    
    {% if 'conditions' in results and results['conditions'] %}
    <h3>Conditions ({{ results['conditions']|length }})</h3>
    <table>
        <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Action</th>
        </tr>
        {% for item in results['conditions'] %}
        <tr>
            <td>{{ item.name }}</td>
            <td>{{ item.description[:100] }}...</td>
            <td><a href="{{ url_for('condition_detail', id=item.id) }}" class="button">View</a></td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
    
    {% if 'medications' in results and results['medications'] %}
    <h3>Medications ({{ results['medications']|length }})</h3>
    <table>
        <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Drug Class</th>
        </tr>
        {% for item in results['medications'] %}
        <tr>
            <td>{{ item.name }}</td>
            <td>{{ item.description[:100] }}...</td>
            <td>{{ item.drug_class }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
    
    {% if 'specialties' in results and results['specialties'] %}
    <h3>Specialties ({{ results['specialties']|length }})</h3>
    <table>
        <tr>
            <th>Name</th>
            <th>Description</th>
        </tr>
        {% for item in results['specialties'] %}
        <tr>
            <td>{{ item.name }}</td>
            <td>{{ item.description[:100] }}...</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
    
    {% if 'references' in results and results['references'] %}
    <h3>References ({{ results['references']|length }})</h3>
    <table>
        <tr>
            <th>Title</th>
            <th>Authors</th>
            <th>Journal</th>
        </tr>
        {% for item in results['references'] %}
        <tr>
            <td>{{ item.title }}</td>
            <td>{{ item.authors }}</td>
            <td>{{ item.journal }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
    
    {% if 'guidelines' in results and results['guidelines'] %}
    <h3>Guidelines ({{ results['guidelines']|length }})</h3>
    <table>
        <tr>
            <th>Title</th>
            <th>Organization</th>
            <th>Summary</th>
        </tr>
        {% for item in results['guidelines'] %}
        <tr>
            <td>{{ item.title }}</td>
            <td>{{ item.organization }}</td>
            <td>{{ item.summary[:100] }}...</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
</div>
{% elif query %}
<div class="card">
    <p>No results found for "{{ query }}"</p>
</div>
{% endif %}
"""

def search_database(db, query, models):
    """
    Search database for query across specified models
    Returns a dictionary of results by model type
    """
    results = {}
    total_results = 0
    
    try:
        # Search conditions
        if 'Condition' in models:
            from models import Condition
            conditions = Condition.query.filter(
                or_(
                    Condition.name.ilike(f'%{query}%'),
                    Condition.description.ilike(f'%{query}%'),
                    Condition.symptoms.ilike(f'%{query}%')
                )
            ).all()
            if conditions:
                results['conditions'] = conditions
                total_results += len(conditions)
        
        # Search medications
        if 'Medication' in models:
            from models import Medication
            medications = Medication.query.filter(
                or_(
                    Medication.name.ilike(f'%{query}%'),
                    Medication.description.ilike(f'%{query}%'),
                    Medication.drug_class.ilike(f'%{query}%'),
                    Medication.side_effects.ilike(f'%{query}%')
                )
            ).all()
            if medications:
                results['medications'] = medications
                total_results += len(medications)
        
        # Search specialties
        if 'Specialty' in models:
            from models import Specialty
            specialties = Specialty.query.filter(
                or_(
                    Specialty.name.ilike(f'%{query}%'),
                    Specialty.description.ilike(f'%{query}%')
                )
            ).all()
            if specialties:
                results['specialties'] = specialties
                total_results += len(specialties)
        
        # Search references
        if 'Reference' in models:
            from models import Reference
            references = Reference.query.filter(
                or_(
                    Reference.title.ilike(f'%{query}%'),
                    Reference.authors.ilike(f'%{query}%'),
                    Reference.journal.ilike(f'%{query}%'),
                    Reference.abstract.ilike(f'%{query}%')
                )
            ).all()
            if references:
                results['references'] = references
                total_results += len(references)
        
        # Search guidelines
        if 'Guideline' in models:
            from models import Guideline
            guidelines = Guideline.query.filter(
                or_(
                    Guideline.title.ilike(f'%{query}%'),
                    Guideline.organization.ilike(f'%{query}%'),
                    Guideline.summary.ilike(f'%{query}%')
                )
            ).all()
            if guidelines:
                results['guidelines'] = guidelines
                total_results += len(guidelines)
        
        return results, total_results
    
    except Exception as e:
        logger.error(f"Error during search: {e}")
        return {}, 0

@search_bp.route('/')
def search_form():
    """Display search form"""
    return render_template_string(
        session.get('base_template', '{{ content | safe }}'),
        content=render_template_string(
            SEARCH_TEMPLATE,
            query='',
            results=None,
            total_results=0
        )
    )

@search_bp.route('/results')
def search_results():
    """Search and display results"""
    query = request.args.get('query', '')
    search_in = request.args.getlist('search_in')
    
    if not query or not search_in:
        return render_template_string(
            session.get('base_template', '{{ content | safe }}'),
            content=render_template_string(
                SEARCH_TEMPLATE,
                query=query,
                results=None,
                total_results=0
            )
        )
    
    # Map search_in values to model classes
    model_map = {
        'conditions': 'Condition',
        'medications': 'Medication',
        'specialties': 'Specialty',
        'references': 'Reference',
        'guidelines': 'Guideline'
    }
    
    models_to_search = [model_map[item] for item in search_in if item in model_map]
    
    # Get database from app context
    from flask import current_app
    db = current_app.extensions['sqlalchemy'].db
    
    # Perform search
    results, total_results = search_database(db, query, models_to_search)
    
    return render_template_string(
        session.get('base_template', '{{ content | safe }}'),
        content=render_template_string(
            SEARCH_TEMPLATE,
            query=query,
            results=results,
            total_results=total_results
        )
    )
