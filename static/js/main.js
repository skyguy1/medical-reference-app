// Main JavaScript for MedRef Application

document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchResultsList = document.getElementById('searchResultsList');
    const closeSearchResults = document.getElementById('closeSearchResults');
    
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInput.value.trim();
            
            if (query.length > 0) {
                performSearch(query);
            }
        });
    }
    
    if (closeSearchResults) {
        closeSearchResults.addEventListener('click', function() {
            searchResults.style.display = 'none';
        });
    }
    
    // Search function
    function performSearch(query) {
        fetch(`/search?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displaySearchResults(data);
            })
            .catch(error => {
                console.error('Error performing search:', error);
            });
    }
    
    // Display search results
    function displaySearchResults(results) {
        searchResultsList.innerHTML = '';
        
        if (results.length === 0) {
            searchResultsList.innerHTML = `
                <div class="alert alert-info">
                    <i class="bi bi-info-circle me-2"></i>No results found for your search.
                </div>
            `;
        } else {
            results.forEach(result => {
                const resultItem = document.createElement('div');
                resultItem.className = 'search-result-item';
                
                let badgeClass = 'bg-secondary';
                let badgeText = result.type;
                let resultUrl = '#';
                
                if (result.type === 'condition') {
                    badgeClass = 'bg-primary';
                    badgeText = 'Condition';
                    resultUrl = `/condition/${result.id}`;
                } else if (result.type === 'medication') {
                    badgeClass = 'bg-success';
                    badgeText = 'Medication';
                    resultUrl = `/medication/${result.id}`;
                } else if (result.type === 'specialty') {
                    badgeClass = 'bg-info';
                    badgeText = 'Specialty';
                    resultUrl = `/specialty/${result.id}`;
                }
                
                resultItem.innerHTML = `
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h4><a href="${resultUrl}" class="text-decoration-none">${result.name}</a></h4>
                            <span class="badge ${badgeClass} me-2">${badgeText}</span>
                            <p>${result.description}</p>
                        </div>
                        <a href="${resultUrl}" class="btn btn-sm btn-outline-primary">View</a>
                    </div>
                `;
                
                searchResultsList.appendChild(resultItem);
            });
        }
        
        searchResults.style.display = 'block';
    }
    
    // Tab functionality for browse page
    const triggerTabList = document.querySelectorAll('#myTab button');
    if (triggerTabList.length > 0) {
        triggerTabList.forEach(triggerEl => {
            const tabTrigger = new bootstrap.Tab(triggerEl);
            
            triggerEl.addEventListener('click', event => {
                event.preventDefault();
                tabTrigger.show();
            });
        });
    }
    
    // Add animation to cards
    const cards = document.querySelectorAll('.card');
    if (cards.length > 0) {
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }
    
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
});
