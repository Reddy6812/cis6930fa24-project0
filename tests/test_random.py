import os
import pytest
import sqlite3
from project0.main import extractincidents, createdb, populatedb, status, fetchincidents

# Sample PDF URL for testing
sample_pdf_url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
db_path = "resources/normanpd.db"

# Expected incidents data for testing
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

@pytest.fixture(scope="module")
def setup_sample_pdf():
    # Ensure the PDF is downloaded before running the tests
    pdf_path = fetchincidents(sample_pdf_url)
    return pdf_path

def test_extractincidents(setup_sample_pdf):
    # Extract incidents from the PDF
    incidents = extractincidents(setup_sample_pdf)

    # Filter out the incidents to match only the expected ones
    filtered_incidents = [
        inc for inc in incidents if inc['incident_number'] in [
            expected['incident_number'] for expected in expected_incidents
        ]
    ]
    
    # Assert the filtered incidents match the expected incidents
    assert len(filtered_incidents) == len(expected_incidents)
    
    # Optional: compare individual incidents if the order is guaranteed
    for i in range(len(expected_incidents)):
        assert filtered_incidents[i]['incident_time'] == expected_incidents[i]['incident_time']
        assert filtered_incidents[i]['incident_number'] == expected_incidents[i]['incident_number']
        assert filtered_incidents[i]['location'] == expected_incidents[i]['location']
        assert filtered_incidents[i]['nature'] == expected_incidents[i]['nature']
        assert filtered_incidents[i]['incident_ori'] == expected_incidents[i]['incident_ori']

def test_createdb_and_populatedb():
    # Test database creation and data insertion
    db_conn = createdb()
    
    # Clear the table to ensure a fresh start
    c = db_conn.cursor()
    c.execute('DELETE FROM incidents')
    db_conn.commit()

    # Populate the database with expected incidents only
    populatedb(db_conn, expected_incidents)
    
    # Query the inserted data
    c.execute('SELECT * FROM incidents')
    rows = c.fetchall()
    
    # Verify the number of rows matches expected incidents
    assert len(rows) == len(expected_incidents)
    
    # Check that each row matches expected incident data
    for i, row in enumerate(rows):
        assert row[0] == expected_incidents[i]['incident_time']
        assert row[1] == expected_incidents[i]['incident_number']
        assert row[2] == expected_incidents[i]['location']
        assert row[3] == expected_incidents[i]['nature']
        assert row[4] == expected_incidents[i]['incident_ori']
    
    # Clean up
    db_conn.close()
    if os.path.exists(db_path):
        os.remove(db_path)

def test_status_output(capsys):
    # Create a test database and insert expected incidents
    db_conn = createdb()
    
    # Clear the table to ensure only our test data is present
    c = db_conn.cursor()
    c.execute('DELETE FROM incidents')
    db_conn.commit()

    # Populate the database with only expected incidents
    populatedb(db_conn, expected_incidents)
    
    # Capture the output of the status function
    status(db_conn)
    
    captured = capsys.readouterr().out.splitlines()
    expected_output = ["Abdominal Pains/Problems|1", "Traffic Stop|1"]
    
    # Extract only relevant lines from captured output
    relevant_lines = [line.strip() for line in captured if '|' in line]
    
    assert relevant_lines == expected_output
    
    # Clean up
    db_conn.close()
    if os.path.exists(db_path):
        os.remove(db_path)
