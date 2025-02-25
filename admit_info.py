from tkinter import *
from tkinter import messagebox
import importlib.util
import sys
from pathlib import Path

users = {}  # Dictionary to store user credentials

# Function to import and run main page
def run_main_page():
    try:
        # Get the path to main_page.py
        main_page_path = Path(__file__).parent / "main_page.py"
        
        # Import main_page.py dynamically
        spec = importlib.util.spec_from_file_location("main_page", main_page_path)
        main_page_module = importlib.util.module_from_spec(spec)
        sys.modules["main_page"] = main_page_module
        spec.loader.exec_module(main_page_module)
        
        # Hide the login window
        win.withdraw()
        
        # Create a function to show login window when main page is closed
        def on_main_close():
            win.deiconify()  # Show login window again
            
        # If main_page has a display_content function, call it
        if hasattr(main_page_module, 'display_content'):
            # Create a new window for the main page
            main_window = Toplevel(win)
            main_window.protocol("WM_DELETE_WINDOW", on_main_close)  # Handle window close
            main_page_module.display_content(main_window)
        else:
            messagebox.showerror("Error", "Main page module is not properly structured")
            win.deiconify()  # Show login window if there's an error
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load main page: {str(e)}")
        win.deiconify()  # Show login window if there's an error

# Function to toggle password visibility
def toggle_password(entry_widget, check_var):
    if check_var.get():
        entry_widget.config(show="")
    else:
        entry_widget.config(show="*")

# Function to check login credentials
def login():
    username = entry_username.get()
    password = entry_password.get()
    if username in users and users[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome {username}!")
        run_main_page()  # Launch main page after successful login
    else:
        messagebox.showerror("Error", "Username or Password is incorrect.")

# Function to handle signup process
def signup():
    fname = entry_fname.get()
    lname = entry_lname.get()
    phone = entry_phone.get()
    username = entry_signup_username.get()
    password = entry_create_password.get()
    confirm_password = entry_confirm_password.get()
    
    if not (fname and lname and phone and username and password and confirm_password):
        messagebox.showerror("Error", "All fields are required")
    elif password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
    elif username in users:
        messagebox.showerror("Error", "Username already exists")
    else:
        users[username] = password
        messagebox.showinfo("Success", f"Account created successfully.\nUsername: {username}\nYou can now log in.")
        show_login_section()

# Function to display the selection section
def show_selection_section(event=None):
    for widget in win.winfo_children():
        if isinstance(widget, Frame):
            widget.destroy()
    
    selection_frame = Frame(win, bg="white", bd=5, relief="ridge")
    selection_frame.place(relx=0.5, rely=0.45, anchor=CENTER, width=400, height=250)
    
    Label(selection_frame, text="Welcome!", font=("Arial", 20), bg="white").pack(pady=10)
    Button(selection_frame, text="Login", command=show_login_section, font=("Arial", 16), bg="blue", fg="white").pack(pady=5)
    Button(selection_frame, text="Sign Up", command=show_signup_section, font=("Arial", 16), bg="green", fg="white").pack(pady=5)

# Function to display the login section
def show_login_section():
    global entry_username, entry_password
    for widget in win.winfo_children():
        if isinstance(widget, Frame):
            widget.destroy()
    
    login_frame = Frame(win, bg="white", bd=5, relief="ridge")
    login_frame.place(relx=0.5, rely=0.45, anchor=CENTER, width=400, height=350)  # Increased height for checkbox
    
    # Adjusting the layout to be side-by-side using grid
    Label(login_frame, text="Username:", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_username = Entry(login_frame, font=("Arial", 14))
    entry_username.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    Label(login_frame, text="Password:", font=("Arial", 14), bg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_password = Entry(login_frame, font=("Arial", 14), show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    
    # Add show password checkbox
    show_pass_var = BooleanVar()
    Checkbutton(login_frame, text="Show Password", variable=show_pass_var, 
                command=lambda: toggle_password(entry_password, show_pass_var),
                bg="white", font=("Arial", 10)).grid(row=2, column=0, columnspan=2, pady=5)
    
    Button(login_frame, text="Login", command=login, font=("Arial", 16), bg="blue", fg="white").grid(row=3, column=0, columnspan=2, pady=10)
    Button(login_frame, text="Back", command=show_selection_section, font=("Arial", 12), bg="white", fg="blue").grid(row=4, column=0, columnspan=2, pady=10)

# Function to display the signup section
def show_signup_section():
    global entry_fname, entry_lname, entry_phone, entry_signup_username, entry_create_password, entry_confirm_password
    for widget in win.winfo_children():
        if isinstance(widget, Frame):
            widget.destroy()
    
    signup_frame = Frame(win, bg="white", bd=5, relief="ridge")
    signup_frame.place(relx=0.5, rely=0.45, anchor=CENTER, width=400, height=500)  # Increased height for checkboxes
    
    # Adjusting the layout to be side-by-side using grid
    Label(signup_frame, text="First Name:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_fname = Entry(signup_frame, font=("Arial", 12))
    entry_fname.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    Label(signup_frame, text="Last Name:", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_lname = Entry(signup_frame, font=("Arial", 12))
    entry_lname.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    
    Label(signup_frame, text="Phone Number:", font=("Arial", 12), bg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_phone = Entry(signup_frame, font=("Arial", 12))
    entry_phone.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    
    Label(signup_frame, text="Username:", font=("Arial", 12), bg="white").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    entry_signup_username = Entry(signup_frame, font=("Arial", 12))
    entry_signup_username.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
    
    Label(signup_frame, text="Create Password:", font=("Arial", 12), bg="white").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    entry_create_password = Entry(signup_frame, font=("Arial", 12), show="*")
    entry_create_password.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
    
    # Add show password checkbox for create password
    show_create_pass_var = BooleanVar()
    Checkbutton(signup_frame, text="Show Password", variable=show_create_pass_var,
                command=lambda: toggle_password(entry_create_password, show_create_pass_var),
                bg="white", font=("Arial", 10)).grid(row=5, column=0, columnspan=2, pady=5)
    
    Label(signup_frame, text="Confirm Password:", font=("Arial", 12), bg="white").grid(row=6, column=0, padx=10, pady=10, sticky="w")
    entry_confirm_password = Entry(signup_frame, font=("Arial", 12), show="*")
    entry_confirm_password.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
    
    # Add show password checkbox for confirm password
    show_confirm_pass_var = BooleanVar()
    Checkbutton(signup_frame, text="Show Password", variable=show_confirm_pass_var,
                command=lambda: toggle_password(entry_confirm_password, show_confirm_pass_var),
                bg="white", font=("Arial", 10)).grid(row=7, column=0, columnspan=2, pady=5)
    
    Button(signup_frame, text="Sign Up", command=signup, font=("Arial", 16), bg="green", fg="white").grid(row=8, column=0, columnspan=2, pady=10)
    Button(signup_frame, text="Back", command=show_selection_section, font=("Arial", 12), bg="white", fg="blue").grid(row=9, column=0, columnspan=2, pady=10)

# Create main window
win = Tk()
win.title("System")

# Load background image
bg_image = PhotoImage(file="background.png")
win.geometry(f"{bg_image.width()}x{bg_image.height()}")

bg_label = Label(win, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Load and place the logo in the top-left corner
logo_image = PhotoImage(file="logo.png")  # Ensure correct path
logo_label = Label(win, image=logo_image, bg="white")
logo_label.place(x=10, y=10)

win.bind("<Return>", show_selection_section)

win.mainloop()
