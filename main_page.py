import tkinter as tk
import home_content
import patient_info
import admit_info
import bill_records
import doctor_info
import doctor_availability
import nurse_info
import staff_info
import facility_management

def display_content(parent_window):
    # Main GUI window setup using the parent window
    parent_window.title("Hospital Management System")
    parent_window.geometry("800x500")
    parent_window.configure(bg="sky blue")

    # Title Label
    title_label = tk.Label(parent_window, text="HOSPITAL MANAGEMENT SYSTEM", 
                          font=("Arial", 26, "bold"), bg="sky blue")
    title_label.pack(side=tk.TOP, pady=10)

    # Main frame to hold buttons and content
    main_frame = tk.Frame(parent_window, bg="sky blue")
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Left-side frame for buttons
    button_frame = tk.Frame(main_frame, bg="sky blue")
    button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Right-side frame for content
    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

    def load_content(module_name):
        try:
            for widget in content_frame.winfo_children():  # Clear previous content
                widget.destroy()
                
            if module_name == "home":
                home_content.display_content(content_frame)
            elif module_name == "patient_info":
                patient_info.load_patient_info(content_frame)
            elif module_name == "admit_info":
                admit_info.display_content(content_frame)
            elif module_name == "bill_records":
                bill_records.display_content(content_frame)
            elif module_name == "doctor_info":
                doctor_info.display_content(content_frame)
            elif module_name == "doctor_availability":
                doctor_availability.display_content(content_frame)
            elif module_name == "nurse_info":
                nurse_info.display_content(content_frame)
            elif module_name == "staff_info":
                staff_info.display_content(content_frame)
            elif module_name == "facility_management":
                facility_management.display_content(content_frame)
            else:
                module = __import__(module_name)
                module.display_content(content_frame)
        except ImportError as e:
            print(f"Import error: {e}")  # Debug print
            error_label = tk.Label(content_frame, 
                                 text=f"Error: Could not load {module_name}", 
                                 font=("Arial", 12))
            error_label.pack()
        except Exception as e:
            print(f"General error: {e}")  # Debug print
            error_label = tk.Label(content_frame, 
                                 text=f"Error: {str(e)}", 
                                 font=("Arial", 12))
            error_label.pack()

    # Buttons for navigation
    buttons = [
        ("Home", "home"),
        ("Patient Information", "patient_info"),
        ("Admit Information", "admit_info"),
        ("Bill Records", "bill_records"),
        ("Doctor Information", "doctor_info"),
        ("Doctor Availability", "doctor_availability"),
        ("Nurse Information", "nurse_info"),
        ("Other Staff Details", "staff_info"),
        ("Facility Management", "facility_management")
    ]

    for text, module in buttons:
        btn = tk.Button(button_frame, text=text, font=("Arial", 12), 
                       width=20, bg="grey", fg="white", 
                       command=lambda m=module: load_content(m))
        btn.pack(pady=5)

    # Exit Button - modified to handle proper cleanup
    def exit_system():
        parent_window.destroy()  # This will trigger the on_main_close callback

    exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 12), 
                           width=20, bg="red", fg="white", 
                           command=exit_system)
    exit_button.pack(pady=10)

    # Load Home content by default
    load_content("home")