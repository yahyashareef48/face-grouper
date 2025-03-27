import tkinter as tk
from tkinter import ttk, filedialog
import os
from PIL import Image, ImageTk

def browse_folder():
    folder_path = filedialog.askdirectory(title="Select Image Folder")
    if folder_path:
        display_images(folder_path)

def display_images(folder_path):
    # Find all image files in the folder
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]
    
    # Print to console
    print(f"Found {len(image_files)} images in {folder_path}")
    for img in image_files:
        print(f" - {img}")
    
    # Display in UI
    # Clear previous images if any
    for widget in images_frame.winfo_children():
        widget.destroy()
    
    # Add a label showing the count of images
    count_label = ttk.Label(images_frame, text=f"Displaying all {len(image_files)} images")
    count_label.pack(side=tk.TOP, pady=10)
    
    # Create a container frame for all images
    thumbnail_frame = ttk.Frame(images_frame)
    thumbnail_frame.pack(fill=tk.BOTH, expand=True)
    
    # Use a grid layout to better organize images
    row, col = 0, 0
    max_cols = 5  # Number of thumbnails per row
    
    # Load and display all thumbnail images
    for i, img_file in enumerate(image_files):
        img_path = os.path.join(folder_path, img_file)
        try:
            # Create thumbnail - use more efficient loading
            img = Image.open(img_path)
            img.thumbnail((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            
            # Create frame for image and label
            img_frame = ttk.Frame(thumbnail_frame)
            img_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Display image
            img_label = ttk.Label(img_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            img_label.pack()
            
            # Display filename
            name_label = ttk.Label(img_frame, text=img_file[:15] + "..." if len(img_file) > 15 else img_file)
            name_label.pack()
            
            # Update row and column for grid layout
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
            # Update UI every 20 images to keep it responsive
            if i % 20 == 0:
                root.update()
                
        except Exception as e:
            print(f"Error loading {img_file}: {e}")

def main():
    global images_frame, root  # Make them accessible in display_images function
    
    # Create the main window
    root = tk.Tk()
    root.title("Face Grouper")
    root.geometry("800x600")  # Set window size
    
    # Add some content
    label = ttk.Label(root, text="Welcome to Face Grouper", font=("Arial", 18))
    label.pack(pady=20)
    
    # Add a button
    button = ttk.Button(root, text="Browse Images", command=browse_folder)
    button.pack(pady=20)
    
    # Create a scrollable container
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Add scrollbars - both vertical and horizontal
    v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical")
    h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal")
    canvas = tk.Canvas(main_frame)
    
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Configure scrollbars
    v_scrollbar.config(command=canvas.yview)
    h_scrollbar.config(command=canvas.xview)
    canvas.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    canvas.config(scrollregion=(0, 0, 500, 500))
    
    # Create frame for images inside canvas
    images_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=images_frame, anchor="nw")
    
    # Update scroll region when the size of the frame changes
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    images_frame.bind("<Configure>", on_frame_configure)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()