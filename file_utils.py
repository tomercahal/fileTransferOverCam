import os
import tkinter as tk
from tkinter import filedialog

def select_file_to_send():
    """Open file dialog to select a file for transfer"""
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

def read_file_data(file_path):
    """Read file data and return filename and data"""
    if not file_path:
        return None, b""
    
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    return file_name, file_data

def select_save_directory():
    """Let the user choose the directory to save the received file"""    
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

def save_file_data(directory, filename, data):
    """Save file data to specified directory and return full path"""
    save_path = os.path.join(directory, filename)
    with open(save_path, "wb") as f:
        f.write(data)
    return save_path

def open_file_after_save(file_path):
    """Open the saved file with the default system application"""
    try:
        os.startfile(file_path)
    except Exception as e:
        print(f"Could not open file: {e}")