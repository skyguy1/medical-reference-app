import webbrowser
import time
import sys

def open_url(url, delay=2):
    """Open a URL in the default web browser"""
    print(f"Opening URL: {url}")
    webbrowser.open(url)
    time.sleep(delay)  # Wait a bit between opening URLs

if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"
    
    # First open the main page
    open_url(f"{base_url}/")
    
    # Then open some medication pages
    medications = [
        "Lisinopril",
        "Levetiracetam",
        "Isotretinoin",
        "Fluoxetine (Prozac)",
        "Insulin Glargine"
    ]
    
    for medication in medications:
        med_url = f"{base_url}/medication/{medication}"
        open_url(med_url)
        
    print("All URLs have been opened in your default web browser.")
