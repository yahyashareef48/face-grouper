import os
import face_recognition
from PIL import Image, ImageDraw
import numpy as np
from collections import defaultdict

class FaceGrouper:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.grouped_faces = defaultdict(list)
        self.tolerance = 0.6  # Face matching tolerance - lower is more strict

    def process_image(self, image_path):
        """Process a single image to find and encode faces"""
        try:
            # Load the image
            image = face_recognition.load_image_file(image_path)
            
            # Find all face locations in the image
            face_locations = face_recognition.face_locations(image)
            
            # If no faces found, return empty list
            if not face_locations:
                print(f"No faces found in {image_path}")
                return []
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            return {
                'path': image_path,
                'locations': face_locations,
                'encodings': face_encodings
            }
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return []
            
    def group_faces(self, image_files):
        """Group faces across multiple images"""
        self.known_face_encodings = []
        self.known_face_names = []
        self.grouped_faces = defaultdict(list)
        
        # Process all images
        results = []
        for i, (filename, filepath) in enumerate(image_files):
            print(f"Processing image {i+1}/{len(image_files)}: {filename}")
            result = self.process_image(filepath)
            if result:
                results.append((filename, result))
        
        # Group similar faces
        face_id = 1
        
        for filename, result in results:
            face_found = False
            for i, face_encoding in enumerate(result['encodings']):
                # Compare with known faces
                matches = face_recognition.compare_faces(
                    self.known_face_encodings, face_encoding, tolerance=self.tolerance
                ) if self.known_face_encodings else []
                
                # If we found a match
                if True in matches:
                    matched_face_idx = matches.index(True)
                    face_name = self.known_face_names[matched_face_idx]
                    face_found = True
                else:
                    # This is a new face
                    face_name = f"Person_{face_id}"
                    face_id += 1
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(face_name)
                    face_found = True
                
                # Add to grouped faces
                face_location = result['locations'][i]
                self.grouped_faces[face_name].append({
                    'filename': filename,
                    'filepath': result['path'],
                    'location': face_location
                })
        
        return self.grouped_faces
    
    def label_faces(self, output_dir):
        """Save labeled images to output directory"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        labeled_images = {}
        
        for person, faces in self.grouped_faces.items():
            for face_info in faces:
                filepath = face_info['filepath']
                filename = face_info['filename']
                
                # Only process each image once
                if filepath in labeled_images:
                    continue
                
                try:
                    # Load image
                    image = face_recognition.load_image_file(filepath)
                    pil_image = Image.fromarray(image)
                    draw = ImageDraw.Draw(pil_image)
                    
                    # Find all faces in this image
                    for person_name, person_faces in self.grouped_faces.items():
                        for face in person_faces:
                            if face['filepath'] == filepath:
                                # Draw rectangle and label
                                top, right, bottom, left = face['location']
                                draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0), width=2)
                                draw.rectangle(((left, bottom - 20), (right, bottom)), fill=(0, 255, 0))
                                draw.text((left + 6, bottom - 17), person_name, fill=(255, 255, 255))
                    
                    # Save the image
                    output_path = os.path.join(output_dir, f"labeled_{filename}")
                    pil_image.save(output_path)
                    labeled_images[filepath] = output_path
                except Exception as e:
                    print(f"Error labeling image {filepath}: {e}")
        
        return labeled_images
    
    def get_summary(self):
        """Return a summary of the face grouping"""
        summary = {
            'total_people': len(self.grouped_faces),
            'people': []
        }
        
        for person, faces in self.grouped_faces.items():
            person_info = {
                'name': person,
                'count': len(faces),
                'images': [face['filename'] for face in faces]
            }
            summary['people'].append(person_info)
            
        return summary
