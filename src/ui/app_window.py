import tkinter as tk
from tkinter import ttk
# Use absolute imports
from ui.image_gallery import ImageGallery
from utils.file_handler import select_image_folder

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
        browse_button.pack(side=tk.LEFT, pady=5)
        
        # Create the image gallery
        self.gallery = ImageGallery(self.root)
        
    def browse_for_images(self):
        folder_path = select_image_folder()
        if folder_path:
            self.gallery.load_and_display_images(folder_path)
