import tkinter as tk

def display_content(frame):
    # Clear previous content
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create a canvas and set background image
    canvas = tk.Canvas(frame)
    canvas.pack(fill="both", expand=True)  # Make sure canvas fills the entire frame
        
    bg_image = tk.PhotoImage(file="home_content.png")  # Ensure correct path
    canvas.create_image(0, 0, anchor='nw', image=bg_image)  # Place image at the top-left
    canvas.config(width=frame.winfo_width(), height=frame.winfo_height())  # Make the canvas the same size as the frame
    canvas.image = bg_image  # Keep reference to the image
    
    # Title label - centered at top
    title_label = tk.Label(frame, text="Welcome To Evergreen Hospital!", 
                          font=("Arial", 26, "bold"), bg='white')
    title_label.place(relx=0.5, rely=0.1, anchor='n')  # Centered at top
    
    # Load and display logo - centered
    logo_image = tk.PhotoImage(file="logo.png")
    logo_label = tk.Label(frame, image=logo_image, bg='white')
    logo_label.image = logo_image
    logo_label.place(relx=0.5, rely=0.2, anchor='n')  # Centered below the title
    
   # Contact details below the logo
    contact_frame = tk.Frame(frame, bg='white')
    contact_frame.place(relx=0.5, rely=0.8, anchor='n')  # Positioned below logo
    
    # Contact details - stacked below logo
    email_label = tk.Label(contact_frame, text="@evergreenhospital.gmail.com", font=("Arial", 12), bg='white')
    email_label.pack(pady=5)
    
    contact_label = tk.Label(contact_frame, text="Contact info: +1 9100718 / 9876123", font=("Arial", 12), bg='white')
    contact_label.pack(pady=5)
    
    service_label = tk.Label(contact_frame, text="At your service 24/7", font=("Arial", 12, "italic"), bg='white')
    service_label.pack(pady=5)
