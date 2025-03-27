import tkinter as tk
from tkinter import ttk
# Use absolute import
from utils.image_processor import get_image_thumbnails, get_face_group_thumbnails

class ImageGallery:
    def __init__(self, parent):
        self.parent = parent
        self.current_image_files = []
        self.setup_gallery()
        
    def setup_gallery(self):
        # Create a scrollable container
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Add scrollbars
        self.v_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical")
        self.h_scrollbar = ttk.Scrollbar(self.main_frame, orient="horizontal")
        self.canvas = tk.Canvas(self.main_frame)
        
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        self.v_scrollbar.config(command=self.canvas.yview)
        self.h_scrollbar.config(command=self.canvas.xview)
        self.canvas.config(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        # Create frame for images inside canvas
        self.images_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.images_frame, anchor="nw")
        
        # Update scroll region when the size of the frame changes
        self.images_frame.bind("<Configure>", self.on_frame_configure)
        
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def load_and_display_images(self, folder_path):
        # Clear previous images
        for widget in self.images_frame.winfo_children():
            widget.destroy()
            
        # Get image files from the folder
        from utils.file_handler import get_image_files
        self.current_image_files = get_image_files(folder_path)
        images_info = get_image_thumbnails(folder_path)
        
        if not images_info:
            ttk.Label(self.images_frame, text="No images found in the selected folder").pack(pady=20)
            return
            
        # Add a label showing the count of images
        count_label = ttk.Label(self.images_frame, text=f"Displaying all {len(images_info)} images")
        count_label.pack(side=tk.TOP, pady=10)
        
        # Create a container frame for all images
        thumbnail_frame = ttk.Frame(self.images_frame)
        thumbnail_frame.pack(fill=tk.BOTH, expand=True)
        
        # Use a grid layout to better organize images
        row, col = 0, 0
        max_cols = 5  # Number of thumbnails per row
        
        # Load and display all thumbnail images
        for i, (filename, thumbnail) in enumerate(images_info):
            # Create frame for image and label
            img_frame = ttk.Frame(thumbnail_frame)
            img_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Display image
            img_label = ttk.Label(img_frame, image=thumbnail)
            img_label.image = thumbnail  # Keep a reference to prevent garbage collection
            img_label.pack()
            
            # Display filename
            name_label = ttk.Label(img_frame, text=filename[:15] + "..." if len(filename) > 15 else filename)
            name_label.pack()
            
            # Update row and column for grid layout
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
            # Update UI every 20 images to keep it responsive
            if i % 20 == 0:
                self.parent.update()
    
    def display_face_groups(self, grouped_faces):
        """Display face groups in the gallery"""
        # Clear previous content
        for widget in self.images_frame.winfo_children():
            widget.destroy()
            
        # Get thumbnails for each face group
        from utils.image_processor import get_face_group_thumbnails
        group_thumbnails = get_face_group_thumbnails(grouped_faces)
        
        if not group_thumbnails:
            ttk.Label(self.images_frame, text="No face groups found").pack(pady=20)
            return
            
        # Add a label showing the count of groups
        count_label = ttk.Label(self.images_frame, text=f"Displaying {len(group_thumbnails)} face groups")
        count_label.pack(side=tk.TOP, pady=10)
        
        # Create a container for all groups
        groups_container = ttk.Frame(self.images_frame)
        groups_container.pack(fill=tk.BOTH, expand=True)
        
        # For each face group
        for i, (person_name, faces) in enumerate(group_thumbnails.items()):
            # Create a frame for this group
            group_frame = ttk.LabelFrame(groups_container, text=person_name)
            group_frame.pack(fill=tk.X, expand=True, padx=10, pady=5, anchor="n")
            
            # Display face count
            count_text = f"{len(faces)} samples shown (out of {len(grouped_faces[person_name])} total)"
            ttk.Label(group_frame, text=count_text).pack(side=tk.TOP, anchor="w", padx=5)
            
            # Create container for face thumbnails
            faces_frame = ttk.Frame(group_frame)
            faces_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Display each face in this group
            for j, (filename, thumbnail) in enumerate(faces):
                face_frame = ttk.Frame(faces_frame)
                face_frame.pack(side=tk.LEFT, padx=5, pady=5)
                
                # Display face thumbnail
                face_label = ttk.Label(face_frame, image=thumbnail)
                face_label.image = thumbnail  # Keep a reference
                face_label.pack()
                
                # Display filename
                name_label = ttk.Label(face_frame, text=filename[:10] + "..." if len(filename) > 10 else filename)
                name_label.pack()
            
            # Update UI regularly
            if i % 5 == 0:
                self.parent.update()
