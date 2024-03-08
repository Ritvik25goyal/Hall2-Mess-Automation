import csv
import sqlite3
import pickle  # Import pickle for serialization
import urllib.request
import os
db_name = "messdata.db"
table_name = "students"

# Connect to the database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create the students table with DailyPurchases as BLOB
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
  Rollno INTEGER PRIMARY KEY,
  Name TEXT,
  RoomNo TEXT,
  TotalAmount REAL DEFAULT 0.0,
  DailyPurchases BLOB
);
"""
cursor.execute(create_table_query)

# Updating SQlite Database
with open("students.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row if it exists
    next(reader, None)

    # Prepare an UPDATE query to update existing entries
    update_query = f"""
    UPDATE {table_name}
    SET Name = ?, RoomNo = ?
    WHERE Rollno = ?
    """

    for row in reader:
        rollno, name, roomno = row  # Assuming CSV data has Rollno, Name, and RoomNo

        # Try inserting the row. If a duplicate Rollno is found, update instead.
        try:
            cursor.execute(f"INSERT INTO {table_name} (Rollno, Name , RoomNo) VALUES (?, ?, ?)", (rollno, name, roomno))
        except sqlite3.IntegrityError:
            # Duplicate Rollno found, update existing entry
            cursor.execute(update_query, (name, roomno, rollno))
            print(f"Updated existing entry for Rollno: {rollno}")

#Update PhotosDatabase
with open("students.csv","r") as csvfile:
    csv_reader = csv.reader(csvfile)
    # Skip the first row (optional)
    next(csv_reader)  # Read and discard the first row
    folder_path= "StudentImages"
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Folder created: {folder_path}")
        except OSError as error:
            print(f"Error creating folder: {error}")    


    for row in csv_reader:
        filepath  = f"./StudentImages/{row[0]}_0.jpg"
        url = f"https://oa.cc.iitk.ac.in/Oa/Jsp/Photo/{row[0]}_0.jpg"
        if os.path.exists(filepath):
            continue
        else:
            try:
                with urllib.request.urlopen(url) as response, open(filepath, 'wb') as f:
                    f.write(response.read())
                print(f"File downloaded: {filepath}")
            except urllib.error.URLError as e:
                print(f"Error downloading file: {e}")

conn.commit()
conn.close()

print(f"Data imported from CSV to {db_name} database!")