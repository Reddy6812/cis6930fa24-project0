import os
import sys
import sqlite3
import pytest
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../project0')))
from main import extractincidents, createdb, populatedb, status

# Sample PDF and database paths
sample_pdf_path = "sampledata/sample_incident_summary.pdf"
db_path = "resources/normanpd.db"

# Expected incident data
expected_incidents = [
    {
        "incident_time": "8/1/2024 0:04",
        "incident_number": "2024-00055419",
        "location": "1345 W LINDSEY ST",
        "nature": "Traffic Stop",
        "incident_ori": "OK0140200"
    },
    {
        "incident_time": "8/1/2024 11:16",
        "incident_number": "2024-00015398",
        "location": "900 N PORTER AVE",
        "nature": "Abdominal Pains/Problems",
        "incident_ori": "EMSSTAT"
    }
]

def test_extractincidents():
    # Test extraction from PDF
    incidents = extractincidents(sample_pdf_path)
    assert len(incidents) == len(expected_incidents)
    assert incidents == expected_incidents

def test_createdb_and_populatedb():
    # Test DB creation and data insertion
    db_conn = createdb()
    populatedb(db_conn, expected_incidents)
    
    c = db_conn.cursor()
    c.execute('SELECT * FROM incidents')
    rows = c.fetchall()
    
    # Verify the number of rows matches expected incidents
    assert len(rows) == len(expected_incidents)
    
    db_conn.close()
    if os.path.exists(db_path):
        os.remove(db_path)

def test_status_output(capsys):
    # Test the status function output
    db_conn = createdb()
    populatedb(db_conn, expected_incidents)
    
    status(db_conn)
    
    captured = capsys.readouterr()
    expected_output = "Abdominal Pains/Problems|1\nTraffic Stop|1\n"
    assert captured.out == expected_output
    
    db_conn.close()
    if os.path.exists(db_path):
        os.remove(db_path)
