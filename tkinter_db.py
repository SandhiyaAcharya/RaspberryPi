import sqlite3
import tkinter as tk
from tkinter import messagebox

# Function to insert data into the database
def submit_data():
    name = name_entry.get()
    age = age_entry.get()

    if name and age.isdigit():  # Ensure age is a number
        conn = sqlite3.connect("mydb.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mytable (name, age) VALUES (?, ?)", (name, int(age)))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Data inserted successfully!")

        # Clear input fields
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)

    else:
        messagebox.showerror("Error", "Please enter a valid name and age.")

# Database setup
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS mytable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")
conn.commit()
conn.close()

# Create GUI window
root = tk.Tk()
root.title("User Data Entry")
root.geometry("400x250")
root.configure(bg="#f0f0f0")  # Set background color

tk.Label(root, text="", bg="#f0f0f0").grid(row=0, column=0, columnspan=2)

# Input Fields (Using Grid Layout)
tk.Label(root, text="Enter Name:", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#0c3054").grid(row=1, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(root, font=("Arial", 12), width=25)
name_entry.grid(row=1, column=1, padx=10, pady=5)

# Empty Row for Spacing
tk.Label(root, text="", bg="#f0f0f0").grid(row=2, column=0, columnspan=2)

tk.Label(root, text="Enter Age:", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#0c3054").grid(row=3, column=0, padx=10, pady=5, sticky="w")
age_entry = tk.Entry(root, font=("Arial", 12), width=25)
age_entry.grid(row=3, column=1, padx=10, pady=5)

# Empty Row for Spacing
tk.Label(root, text="", bg="#f0f0f0").grid(row=4, column=0, columnspan=2)

# Submit Button
submit_btn = tk.Button(root, text="Submit", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
                       activebackground="#45a049", activeforeground="white", padx=10, pady=5, command=submit_data)
submit_btn.grid(row=5, column=0, columnspan=2, pady=10)

# Run the GUI loop
root.mainloop()
