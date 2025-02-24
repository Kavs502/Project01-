import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def display_content(content_frame):
    bill_info = BillInfo(content_frame)

class BillInfo:
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.create_bill_table()
        self.create_widgets()
        
    def create_bill_table(self):
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                bill_id TEXT PRIMARY KEY,
                name TEXT,
                disease TEXT,
                phone TEXT,
                doctor_charges REAL,
                treatment_charges REAL,
                room_charges REAL,
                total REAL
            )
        ''')
        conn.commit()
        conn.close()

    def clear_entries(self):
        for entry in [self.id_entry, self.name_entry, self.disease_entry, 
                     self.phone_entry, self.doctor_charges_entry, 
                     self.treatment_charges_entry, self.room_charges_entry]:
            entry.delete(0, tk.END)
        self.total_entry.config(state='normal')
        self.total_entry.delete(0, tk.END)
        self.total_entry.config(state='readonly')

    def calculate_total(self):
        try:
            doctor_charges = float(self.doctor_charges_entry.get() or 0)
            treatment_charges = float(self.treatment_charges_entry.get() or 0)
            room_charges = float(self.room_charges_entry.get() or 0)
            total = doctor_charges + treatment_charges + room_charges
            return total
        except ValueError:
            return 0

    def add_bill(self):
        try:
            total = self.calculate_total()
            
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            
            values = (
                self.id_entry.get(),
                self.name_entry.get(),
                self.disease_entry.get(),
                self.phone_entry.get(),
                self.doctor_charges_entry.get(),
                self.treatment_charges_entry.get(),
                self.room_charges_entry.get(),
                total
            )
            
            if any(not str(value).strip() for value in values[:-1]):  # Exclude total from check
                messagebox.showerror("Error", "All fields are required!")
                return
                
            cursor.execute('''
                INSERT INTO bills (
                    bill_id, name, disease, phone, doctor_charges,
                    treatment_charges, room_charges, total
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)
            
            conn.commit()
            conn.close()
            
            self.clear_entries()
            self.display_records()
            messagebox.showinfo("Success", "Bill record added successfully!")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Bill ID already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_bill(self):
        try:
            if not self.id_entry.get():
                messagebox.showerror("Error", "Please enter Bill ID!")
                return
                
            total = self.calculate_total()
            conn = sqlite3.connect('hospital.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE bills 
                SET name=?, disease=?, phone=?, doctor_charges=?,
                    treatment_charges=?, room_charges=?, total=?
                WHERE bill_id=?
            ''', (
                self.name_entry.get(),
                self.disease_entry.get(),
                self.phone_entry.get(),
                self.doctor_charges_entry.get(),
                self.treatment_charges_entry.get(),
                self.room_charges_entry.get(),
                total,
                self.id_entry.get()
            ))
            
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Bill ID not found!")
            else:
                conn.commit()
                self.clear_entries()
                self.display_records()
                messagebox.showinfo("Success", "Bill record updated!")
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_bill(self):
        if not self.id_entry.get():
            messagebox.showerror("Error", "Please enter Bill ID!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this bill record?"):
            try:
                conn = sqlite3.connect('hospital.db')
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM bills WHERE bill_id=?', 
                             (self.id_entry.get(),))
                
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Bill ID not found!")
                else:
                    conn.commit()
                    self.clear_entries()
                    self.display_records()
                    messagebox.showinfo("Success", "Bill record deleted successfully!")
                    
                conn.close()
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bills')
        records = cursor.fetchall()
        
        for record in records:
            self.tree.insert('', 'end', values=record)
            
        conn.close()

    def update_total(self, *args):
        total = self.calculate_total()
        self.total_entry.config(state='normal')
        self.total_entry.delete(0, tk.END)
        self.total_entry.insert(0, f"{total:.2f}")
        self.total_entry.config(state='readonly')

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.content_frame, text="Bill Records", 
                              font=("Arial", 14, "bold"), bg="white")
        title_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        # Main container
        container = tk.Frame(self.content_frame, bg="white")
        container.grid(row=1, column=0, sticky='nsew')
        
        # Left side input frame
        input_frame = tk.Frame(container, bg="white")
        input_frame.grid(row=0, column=0, padx=5, sticky='nw')
        
        # Entry fields
        labels = ['Bill ID:', 'Name:', 'Disease:', 'Phone:', 'Doctor Charges:', 
                 'Treatment Charges:', 'Room Charges:', 'Total:']
        
        # Create labels and entries
        for i, label in enumerate(labels):
            tk.Label(input_frame, text=label, bg="white", 
                    font=("Arial", 10)).grid(row=i, column=0, padx=3, pady=2, sticky='w')
            
            if label == 'Total:':
                self.total_entry = tk.Entry(input_frame, width=28, state='readonly')
                self.total_entry.grid(row=i, column=1, padx=3, pady=2)
            else:
                entry = tk.Entry(input_frame, width=28)
                entry.grid(row=i, column=1, padx=3, pady=2)
                
                if label == 'Bill ID:':
                    self.id_entry = entry
                elif label == 'Name:':
                    self.name_entry = entry
                elif label == 'Disease:':
                    self.disease_entry = entry
                elif label == 'Phone:':
                    self.phone_entry = entry
                elif label == 'Doctor Charges:':
                    self.doctor_charges_entry = entry
                    self.doctor_charges_entry.bind('<KeyRelease>', self.update_total)
                elif label == 'Treatment Charges:':
                    self.treatment_charges_entry = entry
                    self.treatment_charges_entry.bind('<KeyRelease>', self.update_total)
                elif label == 'Room Charges:':
                    self.room_charges_entry = entry
                    self.room_charges_entry.bind('<KeyRelease>', self.update_total)

        # Buttons frame
        button_frame = tk.Frame(container, bg="white")
        button_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        tk.Button(button_frame, text="Add", command=self.add_bill, 
                  width=8, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=3)
        tk.Button(button_frame, text="Update", command=self.update_bill, 
                  width=8, bg="#2196F3", fg="white").grid(row=0, column=1, padx=3)
        tk.Button(button_frame, text="Delete", command=self.delete_bill, 
                  width=8, bg="#f44336", fg="white").grid(row=0, column=2, padx=3)
        
        # Treeview frame
        tree_frame = tk.Frame(container, bg="white")
        tree_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky='nsew')
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Name', 'Disease', 'Phone', 'Doctor Charges', 
                  'Treatment Charges', 'Room Charges', 'Total')
        
        self.tree = ttk.Treeview(tree_frame, 
            columns=columns,
            show='headings', 
            yscrollcommand=tree_scroll.set,
            height=25)
        
        tree_scroll.config(command=self.tree.yview)
        
        # Column settings
        widths = [30, 100, 100, 100, 100, 110, 100, 70]
        
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