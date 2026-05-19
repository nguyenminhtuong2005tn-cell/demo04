import requests
import csv
from io import StringIO

# Download CSV data
url = 'https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b'
response = requests.get(url)
response.raise_for_status()
response.encoding = 'utf-8'
csv_text = response.text

# Parse CSV
reader = csv.reader(StringIO(csv_text))
rows = list(reader)

# Summary
row_count = len(rows) - 1  # Exclude header
col_count = len(rows[0]) if rows else 0
print(f"總列數 (Total rows): {row_count}")
print(f"欄位數 (Column count): {col_count}\n")

# Field labels
labels = [
    "Id", "Status", "Name", "Description", "Participation", "Location", "Add", "Tel", "Org", "Start", "End", "Cycle", "Noncycle", "Map", "Px", "Py", "Travellinginfo", "Parkinginfo", "Charge", "Remarks", "Changetime"
]

# Print 1st record with labels
if row_count > 0:
    first_record = rows[1]
    print("第1筆資料 (First record):")
    for label, value in zip(labels, first_record):
        print(f"{label}: {value}")
else:
    print("No data rows found.")
