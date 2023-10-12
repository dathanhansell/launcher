import ctypes
import ctypes.util
import math
import tkinter as tk
import subprocess
import keyboard
from win32api import GetSystemMetrics, GetCursorPos
from PIL import ImageTk, Image
import os
import time
from tkinterdnd2 import DND_FILES, TkinterDnD

app_paths = [
    "C:\\Program Files\\paint.net\\PaintDotNet.exe",
    "C:\\Users\\Dathan\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "C:\\Users\\Dathan\\AppData\\Local\\Programs\\xyz.chatboxapp.app\\Chatbox.exe"

]

def button_layout(n):
    if n == 1:
        yield (0.5, 0.5) 
    else:
        for i in range(n):
            yield (0.5-0.4*math.sin(2 * math.pi / n * i), 0.5-0.4*math.cos(2 * math.pi / n * i))



def open_app(path):
    def opener():
        try:
            subprocess.Popen(path)
            toggle_visibility()
            print(f"App opened with path: {path}")
        except Exception as e:
            print(f"Failed to open app with path: {path}. Reason: {str(e)}")
    return opener

from icoextract import IconExtractor

def extract_icon(path):
    try:
        ie = IconExtractor(path)
        icon_path = "temp_icon.ico"
        ie.export_icon(icon_path)
        time.sleep(1)  # Wait for the icon extraction is complete
        icon = Image.open(icon_path)
        icon.thumbnail((64, 64))
        #read file data and immediately close the file
        img = ImageTk.PhotoImage(icon)
        icon.close()
        os.remove(icon_path)
        return img
    except Exception as e:
        print(f"Couldn't extract icon from path {path}, reason: {str(e)}")

root = TkinterDnD.Tk()  # Instead of tk.Tk()

# Set the window size
WINDOW_SIZE = "400x400"
root.geometry(WINDOW_SIZE)
def drop(event):
    filepath = event.data
    if filepath.lower().endswith('.exe'):
        app_paths.append(filepath)
        
        # Update Buttons on UI with new exe.
        coords = button_layout(len(app_paths))
        root.update()
        image = extract_icon(filepath)
        if image:
            button = tk.Button(root, command=open_app(filepath), bg='white', activebackground='white', bd=0, highlightthickness=0)
            button.image = image  # keep a reference 
            button.config(image=image)
            canvas.create_window(coords[-1][0]*400, coords[-1][1]*400, window=button, anchor='center')
        
    else:
        print('Not an exe file!')
# Make the window appear over all others
root.attributes('-topmost', True)

# Create a transparent window and remove the title bar
root.attributes('-alpha', 1)      
root.overrideredirect(True)

# Update canvas size based on the window size
canvas = tk.Canvas(root, width=400, height=400, bd=0, highlightthickness=0)

canvas.pack()

def toggle_visibility():
    if root.state() == 'normal':
        root.withdraw()
    else:
        x, y = GetCursorPos()
        root.geometry('+%d+%d' % (x-400//2, y-400//2))
        root.update()
        root.deiconify()

keyboard.add_hotkey('ctrl + space', toggle_visibility)
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)
coords = button_layout(len(app_paths))
coords = list(coords)


root.update() # Add this after defining coords.
for path, coord in zip(app_paths, coords):
    app_name = path.split("\\")[-1] 
    image = extract_icon(path)
    if image:
        button = tk.Button(root, command=open_app(path), bg='white', activebackground='white', bd=0, highlightthickness=0)
        button.image = image  # keep a reference 
        button.config(image=image)
        canvas.create_window(coord[0]*400, coord[1]*400, window=button, anchor='center')



root.mainloop()
