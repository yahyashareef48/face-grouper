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

def create_face_thumbnail(image_path, face_location, size=(100, 100)):
    """Create a thumbnail from a face in an image"""
    try:
        # Load the image
        img = Image.open(image_path)
        
        # Extract face coordinates
        top, right, bottom, left = face_location
        
        # Crop the face with a small margin
        margin = 20
        face_img = img.crop((
            max(0, left - margin),
            max(0, top - margin),
            min(img.width, right + margin),
            min(img.height, bottom + margin)
        ))
        
        # Resize to thumbnail
        face_img.thumbnail(size)
        
        # Convert to PhotoImage
        return ImageTk.PhotoImage(face_img)
    except Exception as e:
        print(f"Error creating face thumbnail for {image_path}: {e}")
        return None

def get_face_group_thumbnails(grouped_faces, max_faces_per_group=5):
    """Create thumbnails for each face group"""
    group_thumbnails = {}
    
    for person_name, faces in grouped_faces.items():
        thumbnails = []
        # Limit number of thumbnails per group to avoid memory issues
        for face_info in faces[:max_faces_per_group]:
            thumbnail = create_face_thumbnail(face_info['filepath'], face_info['location'])
            if thumbnail:
                thumbnails.append((face_info['filename'], thumbnail))
        
        group_thumbnails[person_name] = thumbnails
    
    return group_thumbnails
