import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from win32api import GetSystemMetrics, GetCursorPos
from button import Button
from helpers import button_layout, extract_icon, clean_path, folder_icon, parse_paths, executable_path
from config import load_paths, save_path, save_config, load_config, path_exists
from pathlib import Path
import os
import ctypes
from PIL import Image, ImageTk 

class Window:
    def __init__(self):
        print("window")
        self.config = load_config()
        self.radius = self.config.get("radius", 400)
        self.show_labels_on_programs = self.config.get("show_labels_on_programs", False)
        self.show_labels_on_directories = self.config.get("show_labels_on_directories", True)
        self.hide_launcher_on_icon_click = self.config.get("hide_launcher_on_icon_click", True)
        self.enable_hover_effect = self.config.get("enable_hover_effect", True)
        self.config["paths"] = None
        save_config(self.config)

        self.root = TkinterDnD.Tk()
        self.canvas = tk.Canvas(self.root, width=self.radius, height=self.radius, bd=0, highlightthickness=0,bg="DarkSlateGray")

        self.init_window()

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)

        self.preferences_window = None
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Preferences", command=self.show_preferences_menu)
        self.context_menu.add_command(label="Quit", command=self.root.quit)
        self.root.bind("<Button-3>", self.show_context_menu)

    def init_window(self):
        
        self.root.geometry(f"{self.radius+50}x{self.radius+50}")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 1)      
        self.root.wm_attributes("-transparentcolor", "DarkSlateGray")
        self.root.overrideredirect(True)
        self.canvas.config(width=self.radius+50, height=self.radius+50)
        self.canvas.delete("all")
        self.set_background_image()
        # self.canvas.create_oval(0, 0, self.radius, self.radius, fill='#222222')
        self.canvas.pack()

        self.root.withdraw()
        self.buttons = []
        self.initialize_buttons()

    def set_background_image(self):
        # Specify the path to your PNG image
        
        try:
            pil_image = Image.open(executable_path('bg.png'))
            resized_image = pil_image.resize((self.radius, self.radius))
            self.bg_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        except Exception as e:
            print(f"Failed to load background image: {e}")
            # Fallback to a solid color if image loading fails
            self.canvas.create_oval(0, 0, self.radius, self.radius, fill='#222222')

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def show_preferences_menu(self):
        if self.preferences_window is not None and tk.Toplevel.winfo_exists(self.preferences_window):
            self.preferences_window.lift()
            return

        self.preferences_window = tk.Toplevel(self.root)
        self.preferences_window.title("Preferences")

        tk.Label(self.preferences_window, text="Show labels on programs/links").pack(anchor='w')
        self.show_labels_on_programs_var = tk.BooleanVar(value=self.show_labels_on_programs)
        tk.Checkbutton(self.preferences_window, variable=self.show_labels_on_programs_var).pack(anchor='w')

        tk.Label(self.preferences_window, text="Show labels on directories").pack(anchor='w')
        self.show_labels_on_directories_var = tk.BooleanVar(value=self.show_labels_on_directories)
        tk.Checkbutton(self.preferences_window, variable=self.show_labels_on_directories_var).pack(anchor='w')

        tk.Label(self.preferences_window, text="Hide Launcher on Icon Click").pack(anchor='w')
        self.hide_launcher_on_icon_click_var = tk.BooleanVar(value=self.hide_launcher_on_icon_click)
        tk.Checkbutton(self.preferences_window, variable=self.hide_launcher_on_icon_click_var).pack(anchor='w')

        tk.Label(self.preferences_window, text="Enable Hover Effect").pack(anchor='w')
        self.enable_hover_effect_var = tk.BooleanVar(value=self.enable_hover_effect)
        tk.Checkbutton(self.preferences_window, variable=self.enable_hover_effect_var).pack(anchor='w')


        tk.Label(self.preferences_window, text="Radius (pixels)").pack(anchor='w')
        self.radius_var = tk.IntVar(value=self.radius)
        tk.Entry(self.preferences_window, textvariable=self.radius_var).pack(anchor='w')

        tk.Button(self.preferences_window, text="Confirm", command=self.save_preferences).pack(anchor='w')

    def save_preferences(self):
        self.show_labels_on_programs = self.show_labels_on_programs_var.get()
        self.show_labels_on_directories = self.show_labels_on_directories_var.get()
        self.hide_launcher_on_icon_click = self.hide_launcher_on_icon_click_var.get()
        self.enable_hover_effect = self.enable_hover_effect_var.get()
        self.radius = self.radius_var.get()
        self.config["paths"] = None
        self.config["show_labels_on_programs"] = self.show_labels_on_programs
        self.config["show_labels_on_directories"] = self.show_labels_on_directories
        self.config["hide_launcher_on_icon_click"] = self.hide_launcher_on_icon_click
        self.config["enable_hover_effect"] = self.enable_hover_effect
        self.config["radius"] = self.radius
        save_config(self.config)
        self.preferences_window.destroy()
        self.init_window()

    def initialize_buttons(self):
        self.app_paths = load_paths()
        print("init ",self.app_paths,"\n")
        for pathString in self.app_paths:
            self.button_from_path(pathString)

    def toggle_visibility(self):
        if self.root.state() == 'normal':
            self.root.withdraw()
        else:
            x, y = GetCursorPos()
            self.root.geometry('+%d+%d' % (x-self.radius//2, y-self.radius//2))
            self.root.update()
            self.root.deiconify()

    def update_button_positions(self):
        coords = list(button_layout(len(self.app_paths)))
        for button, coord in zip(self.buttons, coords):
            button.window.canvas.coords(button.button_id, coord[0]*self.radius, coord[1]*self.radius)
        self.root.update()

    def drop(self, event):
        paths = parse_paths(event.data)
        for data in paths:
            pathString = clean_path(data)
            if not path_exists(pathString):
                self.button_from_path(pathString)
    
    def append_button(self, button):
        self.buttons.append(button)
        self.update_button_positions() 

    def button_from_path(self,pathString):
        pathString = clean_path(pathString)
        path = Path(pathString)  
        
        if path.is_dir():
            image = folder_icon()
            self.register_path(pathString)
            self.append_button(Button(self, pathString, image, self.open_dir,self.label(pathString,True)))
        else:
            image = extract_icon(pathString)
            if image:
                self.register_path(pathString)
                self.append_button(Button(self, pathString, image, self.open_app,self.label(pathString,False)))
            else:
                print("NOT SUPPORTED ",pathString)

    def open_app(button,self,path):
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", clean_path(path), None, None, 1)
            if self.hide_launcher_on_icon_click:
                self.toggle_visibility()
        except Exception as e:
            print(f"Failed to open app with path: {path}. Reason: {str(e)}")

    def open_dir(button,self,path):
        try:
            os.startfile(path)
            if self.hide_launcher_on_icon_click:
                self.toggle_visibility()
        except Exception as e:
            print(f"Failed to open dir with path: {path}. Reason: {str(e)}")

    def register_path(self,pathString):
            print("add ",os.path.basename(pathString))
            path = save_path(pathString)
            if path != None:
                self.app_paths.append(pathString)

    def label(self,pathString, isDir):
        if isDir:
            if self.show_labels_on_directories:
                return os.path.basename(pathString)
        else:
            if self.show_labels_on_programs:
                return os.path.basename(pathString)