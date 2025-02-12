import sqlite3
import sqlite3
import pandas as pd
import os

# Ensure export folder exists
export_folder = "exportdata"
if not os.path.exists(export_folder):
    os.makedirs(export_folder)

#Connect to SQLite Database (Creates 'mydb.db' if not exists)
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

#Fetch all data from the database
cursor.execute("SELECT * FROM mytable")
rows = cursor.fetchall()

#Convert to DataFrame and Export to Excel
df = pd.DataFrame(rows, columns=["ID", "Name", "Age"])
excel_path = os.path.join(export_folder, "exported_data.xlsx")
df.to_excel(excel_path, index=False)

print(f"Data exported successfully to {excel_path}")

# Close the connection
conn.close()