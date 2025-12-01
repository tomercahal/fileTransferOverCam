try:
    import win32gui
    import win32con
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False
    print("Warning: win32gui not available. Window focusing will not work on Windows.")

def force_focus(window_name):
    """Force focus on the camera window"""
    if not HAS_WIN32:
        print("Window focusing not available - install pywin32 for Windows support")
        return
        
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        try:
            # Bring to front
            win32gui.BringWindowToTop(hwnd)
            # win32gui.SetForegroundWindow(hwnd)
            # Make always on top
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )
            print("Camera window focused and brought to front")
        except Exception as e:
            print(f"Failed to focus window: {e}")
    else:
        print("Camera window not found")