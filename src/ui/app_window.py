import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
# Use absolute imports
from ui.image_gallery import ImageGallery
from utils.file_handler import select_image_folder
from grouper.index import FaceGrouper

class ApplicationWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Grouper")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window size (80% of screen)
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Calculate position for center of screen
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        # Set window geometry
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # Optional: Uncomment to make window maximized by default
        # self.root.state('zoomed')  # For Windows
        # self.root.attributes('-zoomed', True)  # For Linux
        
        # Initialize face grouper
        self.face_grouper = FaceGrouper()
        
        # Store current folder path
        self.current_folder_path = None
        self.current_image_files = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Title
        label = ttk.Label(header_frame, text="Welcome to Face Grouper", font=("Arial", 18))
        label.pack(side=tk.LEFT, pady=10)
        
        # Controls
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Browse button
        browse_button = ttk.Button(controls_frame, text="Browse Images", 
                                  command=self.browse_for_images)
        browse_button.pack(side=tk.LEFT, pady=5, padx=5)
        
        # Group faces button
        self.group_button = ttk.Button(controls_frame, text="Group Faces", 
                                     command=self.group_faces, state=tk.DISABLED)
        self.group_button.pack(side=tk.LEFT, pady=5, padx=5)
        
        # Save labeled images button
        self.save_button = ttk.Button(controls_frame, text="Save Labeled Images", 
                                    command=self.save_labeled_images, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, pady=5, padx=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Please select an image folder to begin")
        status_label = ttk.Label(controls_frame, textvariable=self.status_var)
        status_label.pack(side=tk.RIGHT, pady=5, padx=5)
        
        # Create the image gallery
        self.gallery = ImageGallery(self.root)
        
    def browse_for_images(self):
        folder_path = select_image_folder()
        if folder_path:
            self.current_folder_path = folder_path
            self.gallery.load_and_display_images(folder_path)
            self.current_image_files = self.gallery.current_image_files
            
            # Enable group faces button
            self.group_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.DISABLED)
            self.status_var.set(f"Loaded {len(self.current_image_files)} images. Ready to group faces.")
    
    def group_faces(self):
        if not self.current_image_files:
            messagebox.showinfo("No Images", "Please load images first.")
            return
        
        # Disable buttons during processing
        self.group_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.status_var.set("Processing images... This may take a while.")
        self.root.update()
        
        # Process images and group faces
        try:
            grouped_faces = self.face_grouper.group_faces(self.current_image_files)
            
            # Show summary of grouping
            summary = self.face_grouper.get_summary()
            message = f"Found {summary['total_people']} unique people across {len(self.current_image_files)} images.\n\n"
            
            for person in summary['people']:
                message += f"{person['name']}: {person['count']} appearances\n"
            
            messagebox.showinfo("Face Grouping Results", message)
            
            # Enable save button
            self.save_button.config(state=tk.NORMAL)
            self.status_var.set(f"Completed face grouping. Found {summary['total_people']} unique people.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during face grouping: {e}")
            self.status_var.set("Error during face grouping.")
            self.group_button.config(state=tk.NORMAL)
    
    def save_labeled_images(self):
        if not hasattr(self.face_grouper, 'grouped_faces') or not self.face_grouper.grouped_faces:
            messagebox.showinfo("No Faces Grouped", "Please group faces first.")
            return
        
        # Ask for output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory for Labeled Images")
        if not output_dir:
            return
            
        # Update status
        self.status_var.set("Saving labeled images...")
        self.root.update()
        
        # Save labeled images
        try:
            labeled_images = self.face_grouper.label_faces(output_dir)
            messagebox.showinfo("Success", f"Saved {len(labeled_images)} labeled images to {output_dir}")
            self.status_var.set(f"Saved labeled images to {output_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred when saving labeled images: {e}")
            self.status_var.set("Error saving labeled images.")
