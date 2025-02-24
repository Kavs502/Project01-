import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def display_content(content_frame):
    admit_info = AdmitInfo(content_frame)

class AdmitInfo:
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.create_patient_table()
        self.create_widgets()
        
    def create_patient_table(self):
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT,
                gender TEXT,
                phone NUMBER,
                address TEXT,
                age NUMBER,
                disease TEXT,
                blood_group TEXT,
                check_in TEXT,
                room_number INTEGER,
                doctors TEXT,
                check_out TEXT,
                price TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def clear_entries(self):
        for entry in [self.id_entry, self.name_entry, self.phone_entry, 
                     self.address_entry, self.age_entry, self.disease_entry, 
                     self.checkin_entry, self.room_entry, self.doctors_entry, 
                     self.checkout_entry, self.price_entry]:
            entry.delete(0, tk.END)
        self.gender_combo.set('')
        self.blood_group_combo.set('')

    def add_patient(self):
        try:
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            
            values = (
                self.id_entry.get(),
                self.name_entry.get(),
                self.gender_combo.get(),
                self.phone_entry.get(),
                self.address_entry.get(),
                self.age_entry.get(),
                self.disease_entry.get(),
                self.blood_group_combo.get(),
                self.checkin_entry.get(),
                self.room_entry.get(),
                self.doctors_entry.get(),
                self.checkout_entry.get(),
                self.price_entry.get()
            )
            
            if any(not str(value).strip() for value in values):
                messagebox.showerror("Error", "All fields are required!")
                return
                
            cursor.execute('''
                INSERT INTO patients (
                    patient_id, name, gender, phone, address, age, 
                    disease, blood_group, check_in, room_number, 
                    doctors, check_out, price
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)
            
            conn.commit()
            conn.close()
            
            self.clear_entries()
            self.display_records()
            messagebox.showinfo("Success", "Patient added successfully!")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Patient ID already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_patient(self):
        try:
            if not self.id_entry.get():
                messagebox.showerror("Error", "Please enter Patient ID!")
                return
                
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE patients 
                SET name=?, gender=?, phone=?, address=?, age=?, 
                    disease=?, blood_group=?, check_in=?, room_number=?,
                    doctors=?, check_out=?, price=?
                WHERE patient_id=?
            ''', (
                self.name_entry.get(),
                self.gender_combo.get(),
                self.phone_entry.get(),
                self.address_entry.get(),
                self.age_entry.get(),
                self.disease_entry.get(),
                self.blood_group_combo.get(),
                self.checkin_entry.get(),
                self.room_entry.get(),
                self.doctors_entry.get(),
                self.checkout_entry.get(),
                self.price_entry.get(),
                self.id_entry.get()
            ))
            
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Patient ID not found!")
            else:
                conn.commit()
                self.clear_entries()
                self.display_records()
                messagebox.showinfo("Success", "Patient information updated!")
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_patient(self):
        if not self.id_entry.get():
            messagebox.showerror("Error", "Please enter Patient ID!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this patient?"):
            try:
                conn = sqlite3.connect('hospital.db')
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM patients WHERE patient_id=?', 
                             (self.id_entry.get(),))
                
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Patient ID not found!")
                else:
                    conn.commit()
                    self.clear_entries()
                    self.display_records()
                    messagebox.showinfo("Success", "Patient deleted successfully!")
                    
                conn.close()
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients')
        records = cursor.fetchall()
        
        for record in records:
            self.tree.insert('', 'end', values=record)
            
        conn.close()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.content_frame, text="Admit Information", 
                              font=("Arial", 14, "bold"),bg="white")
        title_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        # Main container
        container = tk.Frame(self.content_frame, bg="white")
        container.grid(row=1, column=0, sticky='nsew')
        
        # Left side input frame
        input_frame = tk.Frame(container, bg="white")
        input_frame.grid(row=0, column=0, padx=5, sticky='nw')
        
        # Entry fields
        labels = ['Patient ID:', 'Name:', 'Gender:', 'Phone:', 'Address:', 
                  'Age:', 'Disease:', 'Blood Group:', 'Check In:', 'Room Number:',
                  'Doctor/s:', 'Check Out:', 'Price:']
        
       #Create labels and entries
        for i, label in enumerate(labels):
            tk.Label(input_frame, text=label, bg="white", 
                    font=("Arial", 10)).grid(row=i, column=0, padx=3, pady=2, sticky='w')
            
            if label == 'Gender:':
                self.gender_combo = ttk.Combobox(input_frame, 
                                               values=['Male', 'Female', 'Other'], 
                                               width=25)
                self.gender_combo.grid(row=i, column=1, padx=3, pady=2)
            elif label == 'Blood Group:':
                self.blood_group_combo = ttk.Combobox(input_frame, 
                    values=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], 
                    width=25)
                self.blood_group_combo.grid(row=i, column=1, padx=3, pady=2)
            else:
                entry = tk.Entry(input_frame, width=28)
                entry.grid(row=i, column=1, padx=3, pady=2)
                
                if label == 'Patient ID:':
                    self.id_entry = entry
                elif label == 'Name:':
                    self.name_entry = entry
                elif label == 'Phone:':
                    self.phone_entry = entry
                elif label == 'Address:':
                    self.address_entry = entry
                elif label == 'Age:':
                    self.age_entry = entry
                elif label == 'Disease:':
                    self.disease_entry = entry
                elif label == 'Check In:':
                    self.checkin_entry = entry
                    self.checkin_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
                elif label == 'Room Number:':
                    self.room_entry = entry
                elif label == 'Doctor/s:':
                    self.doctors_entry = entry
                elif label == 'Check Out:':
                    self.checkout_entry = entry
                    self.checkout_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
                elif label == 'Price:':
                    self.price_entry = entry

       # Buttons frame
        button_frame = tk.Frame(container, bg="white")
        button_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        tk.Button(button_frame, text="Add", command=self.add_patient, 
                  width=8, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=3)
        tk.Button(button_frame, text="Update", command=self.update_patient, 
                  width=8, bg="#2196F3", fg="white").grid(row=0, column=1, padx=3)
        tk.Button(button_frame, text="Delete", command=self.delete_patient, 
                  width=8, bg="#f44336", fg="white").grid(row=0, column=2, padx=3)
        
        # Treeview frame
        tree_frame = tk.Frame(container, bg="")
        tree_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky='nsew')
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Name', 'Gender', 'Phone', 'Address', 'Age', 
                  'Disease', 'Blood Group', 'Check In', 'Room Number', 
                  'Doctor/s', 'Check Out', 'Price')
        
        self.tree = ttk.Treeview(tree_frame, 
            columns=columns,
            show='headings', 
            yscrollcommand=tree_scroll.set,
            height=25)
        
        tree_scroll.config(command=self.tree.yview)
        
        # Column settings
        widths = [10, 40, 40, 40, 40, 20, 40, 70, 50, 80, 50, 30, 30]
        
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