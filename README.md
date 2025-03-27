# Face Grouper

A Python application that groups and labels faces in images using face recognition.

## Features

- Browse and select folders containing images
- Detect faces in images
- Group similar faces across multiple images
- Label faces in images
- Save labeled images to a selected directory

## Requirements

```
click==8.1.8
cmake==3.31.6
colorama==0.4.6
dlib==19.24.1
face-recognition==1.3.0
face_recognition_models==0.3.0
numpy==2.2.4
pillow==11.1.0
```

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python src/main.py`

## Usage

1. Click "Browse Images" to select a folder containing images
2. Click "Group Faces" to detect and group faces
3. Once grouping is complete, click "Save Labeled Images" to save labeled versions of the images

## Development

```
pip freeze > requirements.txt
```
