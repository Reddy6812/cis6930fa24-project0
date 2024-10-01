import argparse
import sqlite3
import urllib.request
import re
import os
import pypdf
from pypdf import PdfReader

def fetchincidents(url):
    # Setting headers for the download request
    h = {
        'User-Agent': ("Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 "
                       "(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17")
    }
    
    # File path for the downloaded PDF
    p = "/tmp/daily_incident_summary.pdf"
    
    try:
        # Requesting and saving the PDF
        r = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(r) as res, open(p, 'wb') as f:
            f.write(res.read())
            
        print(f"PDF downloaded successfully and saved to {p}")
        return p
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return None

def extractincidents(pdf_file_path):
    print("Extracting incidents from the PDF...")
    reader = PdfReader(pdf_file_path)
    incidents = []
    
    # Regex patterns to capture each field
    date_time_pattern = r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2})'
    incident_number_pattern = r'(\d{4}-\d{5,8})'
    location_pattern = r'([A-Z0-9][\w\s./;-]*?|[\d.;-]+|AVE|ST|\d+\s+\d+/\d+|\d+\.\d+;\d+\.\d+)'
    nature_pattern = r'((?:911|Fire|Abdominal\s+)?[A-Z][a-z]+(?:/[A-Za-z]+)*(?:\s+(?:[A-Za-z]+|and|to|Nature\sUnknown|Call))*?)'
    ori_pattern = r'(OK\d+|EMSSTAT|14005)'

    # Combining the full row pattern
    row_pattern = re.compile(
        rf"{date_time_pattern}\s+{incident_number_pattern}\s+{location_pattern}\s+{nature_pattern}\s+{ori_pattern}"
    )

    try:
        for page in reader.pages:
            text = page.extract_text()
            text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
            
            # Find all matches using the improved row pattern
            for match in row_pattern.findall(text):
                incidents.append({
                    "incident_time": match[0].strip(),
                    "incident_number": match[1].strip(),
                    "location": match[2].strip(),
                    "nature": match[3].strip(),
                    "incident_ori": match[4].strip()
                })
        
        print(f"Extracted {len(incidents)} incidents from the PDF.")
        return incidents
    except Exception as e:
        print(f"Error extracting incidents: {e}")
        return []

def createdb():
    print("Creating SQLite database...")
    d = 'resources'
    db_path = os.path.join(d, 'normanpd.db')
    
    # Create 'resources' directory if missing
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"Created directory: {d}")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Creating table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')

    conn.commit()
    print(f"Database created at {db_path}")
    return conn

def populatedb(db, data):
    if not data:
        print("No incidents to insert into the database.")
        return
    
    c = db.cursor()
    # Inserting extracted incidents into the database
    c.executemany('''
        INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
        VALUES (:incident_time, :incident_number, :location, :nature, :incident_ori)
    ''', data)
    
    db.commit()
    print(f"Inserted {len(data)} incidents into the database.")

def status(db):
    c = db.cursor()
    # Fetching and counting incidents by 'nature'
    c.execute('''
        SELECT nature, COUNT(*) as count
        FROM incidents
        GROUP BY nature
        ORDER BY nature ASC
    ''')
    
    results = c.fetchall()
    if not results:
        print("No data available in the database.")
    else:
        for row in results:
            print(f"{row[0]}|{row[1]}")

def main(url):
    # Fetch data
    p = fetchincidents(url)

    if not p:
        print("Failed to download the PDF.")
        return
    
    # Extract incidents
    i = extractincidents(p)
    if not i:
        print("No incidents extracted from the PDF.")
        return
    
    # Create DB
    db = createdb()
    
    # Populate DB
    populatedb(db, i)
    
    # Show status
    status(db)
    db.close()

if __name__ == '__main__':
    # Argument parsing for command line usage
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary URL.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
