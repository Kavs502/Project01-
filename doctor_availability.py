import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def display_content(content_frame):
    doctor_availability = DoctorAvailability(content_frame)

class DoctorAvailability:
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.create_availability_table()
        self.create_widgets()
        
    def create_availability_table(self):
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctor_availability (
                doctor_id TEXT PRIMARY KEY,
                name TEXT,
                gender TEXT,
                age NUMBER,
                phone NUMBER,
                email TEXT,
                level TEXT,
                ward_no INTEGER,
                area TEXT,
                available_at TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def clear_entries(self):
        for entry in [self.id_entry, self.name_entry, self.age_entry, 
                     self.phone_entry, self.email_entry, self.ward_entry]:
            entry.delete(0, tk.END)
        self.gender_combo.set('')
        self.level_combo.set('')
        self.area_combo.set('')
        self.available_at_combo.set('')

    def add_doctor(self):
        try:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            
            values = (
                self.id_entry.get(),
                self.name_entry.get(),
                self.gender_combo.get(),
                self.age_entry.get(),
                self.phone_entry.get(),
                self.email_entry.get(),
                self.level_combo.get(),
                self.ward_entry.get(),
                self.area_combo.get(),
                self.available_at_combo.get()
            )
            
            if any(not str(value).strip() for value in values):
                messagebox.showerror("Error", "All fields are required!")
                return
                
            cursor.execute('''
                INSERT INTO doctor_availability (
                    doctor_id, name, gender, age, phone, email,
                    level, ward_no, area, available_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)
            
            conn.commit()
            conn.close()
            
            self.clear_entries()
            self.display_records()
            messagebox.showinfo("Success", "Doctor availability added successfully!")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Doctor ID already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_doctor(self):
        try:
            if not self.id_entry.get():
                messagebox.showerror("Error", "Please enter Doctor ID!")
                return
                
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE doctor_availability 
                SET name=?, gender=?, age=?, phone=?, email=?,
                    level=?, ward_no=?, area=?, available_at=?
                WHERE doctor_id=?
            ''', (
                self.name_entry.get(),
                self.gender_combo.get(),
                self.age_entry.get(),
                self.phone_entry.get(),
                self.email_entry.get(),
                self.level_combo.get(),
                self.ward_entry.get(),
                self.area_combo.get(),
                self.available_at_combo.get(),
                self.id_entry.get()
            ))
            
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Doctor ID not found!")
            else:
                conn.commit()
                self.clear_entries()
                self.display_records()
                messagebox.showinfo("Success", "Doctor availability updated!")
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_doctor(self):
        if not self.id_entry.get():
            messagebox.showerror("Error", "Please enter Doctor ID!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this doctor's availability?"):
            try:
                conn = sqlite3.connect('hospital.db')
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM doctor_availability WHERE doctor_id=?', 
                             (self.id_entry.get(),))
                
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Doctor ID not found!")
                else:
                    conn.commit()
                    self.clear_entries()
                    self.display_records()
                    messagebox.showinfo("Success", "Doctor availability deleted successfully!")
                    
                conn.close()
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM doctor_availability')
        records = cursor.fetchall()
        
        for record in records:
            self.tree.insert('', 'end', values=record)
            
        conn.close()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.content_frame, text="Doctor Availability", 
                              font=("Arial", 14, "bold"), bg="white")
        title_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        # Main container
        container = tk.Frame(self.content_frame, bg="white")
        container.grid(row=1, column=0, sticky='nsew')
        
        # Left side input frame
        input_frame = tk.Frame(container, bg="white")
        input_frame.grid(row=0, column=0, padx=5, sticky='nw')
        
        # Entry fields
        labels = ['Doctor ID:', 'Name:', 'Gender:', 'Age:', 'Phone:', 'Email:', 
                 'Level:', 'Ward No.:', 'Area:', 'Available At:']
        
        # Create labels and entries
        for i, label in enumerate(labels):
            tk.Label(input_frame, text=label, bg="white", 
                    font=("Arial", 10)).grid(row=i, column=0, padx=3, pady=2, sticky='w')
            
            if label == 'Gender:':
                self.gender_combo = ttk.Combobox(input_frame, 
                                               values=['Male', 'Female', 'Other'], 
                                               width=25)
                self.gender_combo.grid(row=i, column=1, padx=3, pady=2)
            elif label == 'Level:':
                self.level_combo = ttk.Combobox(input_frame,
                                              values=['Senior', 'Junior'],
                                              width=25)
                self.level_combo.grid(row=i, column=1, padx=3, pady=2)
            elif label == 'Area:':
                self.area_combo = ttk.Combobox(input_frame,
                    values=['Cardiology', 'Ophthalmology', 'Oncology', 
                           'Neurology', 'Dermatology', 'Psychology', 
                           'Endocrinology'],
                    width=25)
                self.area_combo.grid(row=i, column=1, padx=3, pady=2)
            elif label == 'Available At:':
                self.available_at_combo = ttk.Combobox(input_frame,
                    values=['9am to 5pm', '9am to 2pm', '2pm to 8pm', 
                           '8pm to 8am', '12am to 12pm'],
                    width=25)
                self.available_at_combo.grid(row=i, column=1, padx=3, pady=2)
            else:
                entry = tk.Entry(input_frame, width=28)
                entry.grid(row=i, column=1, padx=3, pady=2)
                
                if label == 'Doctor ID:':
                    self.id_entry = entry
                elif label == 'Name:':
                    self.name_entry = entry
                elif label == 'Age:':
                    self.age_entry = entry
                elif label == 'Phone:':
                    self.phone_entry = entry
                elif label == 'Email:':
                    self.email_entry = entry
                elif label == 'Ward No.:':
                    self.ward_entry = entry

        # Buttons frame
        button_frame = tk.Frame(container, bg="white")
        button_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        tk.Button(button_frame, text="Add", command=self.add_doctor, 
                  width=8, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=3)
        tk.Button(button_frame, text="Update", command=self.update_doctor, 
                  width=8, bg="#2196F3", fg="white").grid(row=0, column=1, padx=3)
        tk.Button(button_frame, text="Delete", command=self.delete_doctor, 
                  width=8, bg="#f44336", fg="white").grid(row=0, column=2, padx=3)
        
        # Treeview frame
        tree_frame = tk.Frame(container, bg="white")
        tree_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky='nsew')
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Name', 'Gender', 'Age', 'Phone', 'Email', 
                  'Level', 'Ward No.', 'Area', 'Available At')
        
        self.tree = ttk.Treeview(tree_frame, 
            columns=columns,
            show='headings', 
            yscrollcommand=tree_scroll.set,
            height=25)
        
        tree_scroll.config(command=self.tree.yview)
        
        # Column settings
        widths = [30, 60, 80, 50, 80, 90, 80, 80, 80, 100]
        
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        self.tree.pack(side='left', fill='both', expand=True)
        
        # Configure grid weights
        container.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Display initial records
        self.display_records()