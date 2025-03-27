from tkinter import filedialog
import os

def select_image_folder():
    """Open a dialog to select an image folder and return the path"""
    folder_path = filedialog.askdirectory(title="Select Image Folder")
    return folder_path if folder_path else None

def get_image_files(folder_path):
    """Get all image files from a folder"""
    if not folder_path or not os.path.isdir(folder_path):
        return []
        
    # Find all image files in the folder
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]
    
    # Print to console for debugging
    print(f"Found {len(image_files)} images in {folder_path}")
    for img in image_files[:10]:  # Show first 10 for brevity
        print(f" - {img}")
    if len(image_files) > 10:
        print(f" - ... and {len(image_files) - 10} more")
        
    return [(f, os.path.join(folder_path, f)) for f in image_files]
