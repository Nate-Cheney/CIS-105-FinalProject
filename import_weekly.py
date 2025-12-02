import sqlite3
import csv

# Connect to SQLite database (creates if doesn't exist)
conn = sqlite3.connect('data/weekly.db')
cursor = conn.cursor()

# Drop table if exists and create new one
cursor.execute('DROP TABLE IF EXISTS weekly')

# Define headers manually since CSV has no header row
headers = [
    'Player', 'Opp', 'Pts', 'Pass_Att', 'Cmp', 'Pass_Yds', 'Pass_TD', 'Int', 'Pass_2Pt',
    'Rush_Att', 'Rush_Yds', 'Rush_TD', 'Rush_2Pt', 'Rec', 'Rec_Yds', 'Rec_TD', 'Rec_2Pt',
    'FL', 'TD', 'Week'
]

# Create table with all columns as TEXT (SQLite will handle type conversion)
columns = ', '.join([f'"{col}" TEXT' for col in headers])
cursor.execute(f'CREATE TABLE weekly ({columns})')
    
print(f"Created table with columns: {', '.join(headers)}")

# Insert data
with open('data/weekly.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    placeholders = ', '.join(['?' for _ in headers])
    row_count = 0
    
    for row in reader:
        # Remove trailing empty values
        row = [val.strip() if val else None for val in row[:len(headers)]]
        
        # Pad if row is shorter than headers
        if len(row) < len(headers):
            row.extend([None] * (len(headers) - len(row)))
        
        cursor.execute(f'INSERT INTO weekly VALUES ({placeholders})', row)
        row_count += 1
    
    print(f"✓ Imported {row_count} rows into 'weekly' table")

# Commit and close
conn.commit()

# Quick verification
cursor.execute("SELECT COUNT(*) FROM weekly")
count = cursor.fetchone()[0]
print(f"✓ Verified: {count} total rows in database")

cursor.execute("SELECT * FROM weekly LIMIT 3")
print("\nSample data:")
for row in cursor.fetchall():
    print(row[:5])  # Print first 5 columns of each row

conn.close()
print("\n✓ Database saved to data/weekly.db")
