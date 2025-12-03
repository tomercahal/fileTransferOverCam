import os
import tkinter as tk
from tkinter import filedialog

def select_file_to_send():
    """Open file dialog to select a file for transfer, returns the file path"""
    root = tk.Tk()
    root.withdraw()
    
    # Bring dialog to front and make it focused
    root.attributes('-topmost', True)
    root.update()
    
    file_path = filedialog.askopenfilename(
        title="Select file to transfer",
        parent=root
    )
    
    root.destroy()
    return file_path

def select_save_directory():
    """Let the user choose the directory to save the received file, returns the chosen directory path"""    
    root = tk.Tk()
    root.withdraw()

    # Bring dialog to front and make it focused
    root.attributes('-topmost', True)
    root.update()

    directory = filedialog.askdirectory(
        title="Choose the directory to save the file",
        parent=root
    )
    
    root.destroy()            
    if directory:
        return directory
    return os.getcwd()

def read_file_data(file_path):
    """Read file data and return filename and data"""
    if not file_path:
        return None, b""
    
    try:
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_data = f.read()
        return file_name, file_data
    except (FileNotFoundError, PermissionError, OSError) as e:
        return None, b""

def save_file_data(directory, filename, data):
    """Save file data to specified directory and return (path, is_successful)"""
    save_path = os.path.join(directory, filename)
    try:
        with open(save_path, "wb") as f:
            f.write(data)
        return save_path, True
    except (FileNotFoundError, PermissionError, OSError) as e:
        return None, False

def open_file(file_path):
    """Open the the file in the given path"""
    try:
        os.startfile(file_path)
    except Exception as e:
        print(f"Could not open file: {e}")