import os
import sys
import tkinter as tk

# Get the absolute path to the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Add the project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import the application
from ui.app_window import ApplicationWindow

def main():
    # Create and start the application
    root = tk.Tk()
    app = ApplicationWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
