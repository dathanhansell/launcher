import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from win32api import GetSystemMetrics, GetCursorPos
from button import Button
from helpers import button_layout, extract_icon, clean_path
from config import load_paths, save_path

class Window:
    def __init__(self, size="400x400"):
        self.root = TkinterDnD.Tk()
        self.root.geometry(size)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 1)      
        self.root.overrideredirect(True)
        self.canvas = tk.Canvas(self.root, width=400, height=400, bd=0, highlightthickness=0,bg="yellow")
        self.canvas.create_oval(0,0,400,400, fill='#222222')
        self.canvas.pack()
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)
        self.buttons = []
        self.initialize_buttons()

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Quit", command=self.root.quit)
        self.root.bind("<Button-3>", self.show_context_menu)
        self.root.withdraw()
        self.root.wm_attributes("-transparentcolor", "yellow")

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)



    def initialize_buttons(self):
        self.app_paths = load_paths()
        self.coords = list(button_layout(len(self.app_paths)))
        self.root.update()
        for path, coord in zip(self.app_paths, self.coords):
            image = extract_icon(path)
            if image:
                new_button = Button(self, path, coord, image)
                self.buttons.append(new_button)  

    def toggle_visibility(self):
        if self.root.state() == 'normal':
            self.root.withdraw()
        else:
            x, y = GetCursorPos()
            self.root.geometry('+%d+%d' % (x-400//2, y-400//2))
            self.root.update()
            self.root.deiconify()

    def update_button_positions(self):
        new_coords = list(button_layout(len(self.app_paths)))
        for button, coord in zip(self.buttons, new_coords):
            self.canvas.coords(button.button_id, coord[0]*400, coord[1]*400)
        self.root.update()

    def drop(self, event):
        path = clean_path(event.data)        
        image = extract_icon(path)
        if image:
            save_path(path)
            self.app_paths.append(path)
            new_coords = button_layout(len(self.app_paths))
            self.coords.extend(new_coords)
            new_button = Button(self, path, self.coords[-1], image)
            self.buttons.append(new_button)
            self.update_button_positions() 
        else:
            print('Not an exe file!')

