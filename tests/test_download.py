import os
import pytest
from project0.main import fetchincidents

# Sample URL for testing
sample_url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
pdf_file_path = "/tmp/daily_incident_summary.pdf"

def test_fetchincidents():
    # Download the PDF
    downloaded_path = fetchincidents(sample_url)
    
    # Assertions
    assert downloaded_path == pdf_file_path
    assert os.path.exists(downloaded_path)
    
    # Cleanup
    if os.path.exists(downloaded_path):
        os.remove(downloaded_path)
