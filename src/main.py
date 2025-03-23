import tkinter as tk
from tkinter import ttk

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Face Grouper")
    root.geometry("800x600")  # Set window size
    
    # Add some content
    label = ttk.Label(root, text="Welcome to Face Grouper", font=("Arial", 18))
    label.pack(pady=20)
    
    # Add a button
    button = ttk.Button(root, text="Browse Images", command=lambda: print("Button clicked"))
    button.pack(pady=20)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()