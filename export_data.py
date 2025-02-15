import sqlite3
import pandas as pd
import os
from fpdf import FPDF

# Define the base USB mount path
usb_base_path = "/media/pab"

# Check if any USB storage device is mounted inside /media/pab
if not os.path.exists(usb_base_path):
    print("No USB storage mount point found.")
    exit()

# Get list of mounted devices (folders inside /media/pab)
devices = [d for d in os.listdir(usb_base_path) if os.path.isdir(os.path.join(usb_base_path, d))]

if not devices:
    print("No USB storage device found in /media/pab.")
    exit()

# Assume the first detected USB device is the target
usb_device = os.path.join(usb_base_path, devices[0])
export_folder = os.path.join(usb_device, "Exportdata")

print(f"? USB storage device detected: {usb_device}")

# Create Exportdata folder if it doesn't exist
if not os.path.exists(export_folder):
    os.makedirs(export_folder)
    print(f"?? Created folder: {export_folder}")

# Connect to SQLite Database
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

# Fetch all data from the database
cursor.execute("SELECT * FROM mytable")
rows = cursor.fetchall()

# Convert to DataFrame
df = pd.DataFrame(rows, columns=["ID", "Name", "Age"])

# Export to Excel
excel_path = os.path.join(export_folder, "exported_data.xlsx")
df.to_excel(excel_path, index=False)

# Export to PDF
pdf_path = os.path.join(export_folder, "exported_data.pdf")

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        pdf_header = input("Enter the Heading of the PDF: ")
        self.cell(200, 10, pdf_header, ln=True , align="C")
        self.ln(10)  # Line break

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=10)

# Add table headers (center-aligned)
for col in df.columns:
    pdf.cell(50, 10, col, border=1, align="C") 
pdf.ln()

# Add table data (center-aligned)
for row in df.itertuples(index=False):
    for item in row:
        pdf.cell(50, 10, str(item), border=1, align="C")  
    pdf.ln()

pdf.output(pdf_path)

print(f"? Data exported successfully to:\n?? {excel_path}\n?? {pdf_path}")

# Close the connection
conn.close()
