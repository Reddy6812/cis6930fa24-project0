import os
import sys
import pytest
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../project0')))
from main import fetchincidents

# Setup sample URL and file path
sample_url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
pdf_file_path = "/tmp/daily_incident_summary.pdf"

def test_fetchincidents():
    # Test the download function
    downloaded_path = fetchincidents(sample_url)
    assert downloaded_path == pdf_file_path
    assert os.path.exists(downloaded_path)

def teardown_module(module):
    # Clean up the downloaded file
    if os.path.exists(pdf_file_path):
        os.remove(pdf_file_path)
