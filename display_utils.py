import cv2
import numpy as np
import qrcode
import tkinter as tk
try:
    import win32gui
    import win32con
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

# Get screen dimensions once at module load
_root = tk.Tk()
SCREEN_WIDTH = _root.winfo_screenwidth()
SCREEN_HEIGHT = _root.winfo_screenheight()
_root.destroy()

def force_focus(window_name):
    """Force focus on a given window for windows OS"""
    if not HAS_WIN32:
        print("Window focusing not available - install pywin32 for Windows support or manually focus the window once")
        return
        
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        try:
            # Bring to front
            win32gui.BringWindowToTop(hwnd)
            # Make always on top
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )
        except Exception as e:
            print(f"Failed to focus window: {e}")
    else:
        print("Given window not found")

def display_qr_centered(qr_data_string, window_name):
    """Display QR code centered on screen with natural size"""
    qr = qrcode.make(qr_data_string)
    qr_np = np.array(qr.convert('RGB'))
    # Assume QR fits on screen: center the window using the image size
    h, w = qr_np.shape[:2]
    x = max(0, (SCREEN_WIDTH - w) // 2)
    y = max(0, (SCREEN_HEIGHT - h) // 2)

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    try:
        cv2.resizeWindow(window_name, w, h)
    except Exception:
        pass
    try:
        cv2.moveWindow(window_name, x, y)
    except Exception:
        pass

    cv2.imshow(window_name, qr_np)
    cv2.waitKey(1) # Needed to display the window
    force_focus(window_name) # Force focus on QR window after displaying

def close_qr_window(qr_window_name):
    """Close the QR code display window"""
    cv2.destroyWindow(qr_window_name)

def close_all_qr_windows():
    """Close all QR code display windows"""
    cv2.destroyAllWindows()