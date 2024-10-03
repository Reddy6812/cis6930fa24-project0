# cis6930fa24 -- Assignment0

Name: Vijay Kumar Reddy Gade

## Assignment Description 

THIS PROJECT AUTOMATICALLY EXTRACTS INCIDENT DATA FROM THE NORMAN, OKLAHOMA POLICE DEPARTMENT’S INCIDENT REPORT PDF FILES. IT PROCESSES THE INCIDENT INFORMATION AND STORES IT IN A SQLITE DATABASE, WHICH CAN THEN BE QUERIED FOR A SUMMARY OF INCIDENT TYPES. SPECIFIC FIELDS LIKE THE DATE/TIME, INCIDENT NUMBER, LOCATION, NATURE, AND ORI ARE PARSED AND STORED IN A DATABASE.

## HOW TO INSTALL

1. INSTALL PIPENV IF YOU DON'T HAVE IT:
   ```bash
   pip install pipenv
   ```

2. INSTALL THE PROJECT DEPENDENCIES:
   ```bash
   pipenv install
   ```

3. MAKE SURE YOU HAVE `pypdf` INSTALLED VIA THE `PIPFILE`.

## HOW TO RUN

TO RUN THE SCRIPT WITH A SAMPLE PDF URL, USE THE FOLLOWING COMMAND:

```bash
pipenv run python project0/main.py --incidents <URL_OF_INCIDENT_PDF>
```

EXAMPLE:

```bash
pipenv run python project0/main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
```

A DEMO OF THE EXECUTION CAN BE VIEWED BELOW:

![video](demo.gif)

## FUNCTIONS

#### `fetchincidents(url)`
- Downloads the PDF file from the specified URL and saves it locally and returns the path of the saved PDF.

#### `extractincidents(pdf_file_path)`
- Extracts incident information from the PDF and returns A list of dictionaries, each containing incident details like incident time, number, location, nature, and ORI.

#### `createdb()`
- Creates a SQLite database (`normanpd.db`) in the `resources/` directory and returns A connection object to the SQLite database.

#### `populatedb(db, data)`
- Inserts the extracted incident data into the database and SQLite database connection and the extracted incident data.

#### `status(db)`
- Prints a summary of incidents, grouped by nature, in alphabetical order.

## DATABASE DEVELOPMENT

- **Schema**: A table named `incidents` is created with the following columns:
  - `incident_time`: TEXT
  - `incident_number`: TEXT
  - `incident_location`: TEXT
  - `nature`: TEXT
  - `incident_ori`: TEXT

- **Approach**: The data is extracted using regex patterns and parsed into a structured format. It is then inserted into a SQLite database for efficient querying and storage.

## BUGS AND ASSUMPTIONS

- **Bugs**:
  - **Location Formatting Issue**: The current regex patterns may fail to capture locations that are not entirely in uppercase (e.g., `504 N Ponca AV` instead of `504 N PONCA AV`). This issue occurs because the parser expects locations to always be uppercase. This causes failures in parsing locations for incidents where mixed case is used.
  - **Handling of Line Breaks**: If unexpected line breaks occur within the PDF text, some incidents might not be captured correctly.

- **Assumptions**:
  - The format of the incident reports will remain consistent.
  - All location data is expected to be in uppercase.
  - The extracted fields such as date/time, location, and nature will follow a predictable format that can be parsed using regular expressions.

## CHALLENGES

1. **Inconsistent Case in Locations**: Some incident locations use mixed case (e.g., `504 N Ponca AV`), which can lead to failed extraction since the regex expects uppercase. This inconsistency should be accounted for in future versions of the parser.

2. **PDF Format Variability**: If the police department changes how the PDFs are formatted (e.g., changes in text alignment or the order of data), the extraction logic may break, requiring updates to the regex patterns.

## FUTURE IMPROVEMENTS

- **Location Parsing**: Implement more robust location parsing to handle both uppercase and mixed-case locations.
- **Regex Flexibility**: Enhance the regular expressions to better handle edge cases and inconsistencies in the PDF text format.
- **Error Reporting**: Add detailed error logs to better track issues during extraction and database insertion.

---
