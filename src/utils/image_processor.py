from PIL import Image, ImageTk
# Use absolute import
from utils.file_handler import get_image_files

def create_thumbnail(image_path, size=(100, 100)):
    """Create a thumbnail from an image file"""
    try:
        img = Image.open(image_path)
        img.thumbnail(size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        return None

def get_image_thumbnails(folder_path):
    """Get thumbnails for all images in the folder"""
    image_files = get_image_files(folder_path)
    thumbnails = []
    
    for filename, filepath in image_files:
        thumbnail = create_thumbnail(filepath)
        if thumbnail:
            thumbnails.append((filename, thumbnail))
    
    return thumbnails
