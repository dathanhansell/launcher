import tkinter as tk
from tkinter import messagebox
from config import remove_path
from helpers import clean_path
import ctypes
class Button:
    def __init__(self, window, path, coords, image):
        self.window = window  # save parent window reference
        self.path = path
        self.button = tk.Button(window.root, image=image, command=self.open_app, bd=0, bg="#222222", activebackground="#222222")
        self.button.image = image
        self.button.config(image=image)
        self.button.bind("<Button-3>", self.confirm_removal) 
        self.button_id = self.window.canvas.create_window(coords[0]*400, coords[1]*400, 
                                                                  window=self.button, anchor='center')

    def open_app(self):
        try:
            print(self.path)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", clean_path(self.path), None, None, 1)
            self.window.toggle_visibility()
        except Exception as e:
            print(f"Failed to open app with path: {self.path}. Reason: {str(e)}")


    def confirm_removal(self, event):
        if messagebox.askokcancel("Remove Button", "Do you really want to delete this button?", parent=self.window.root):
            self.remove_button()
        return "break"
    
    def remove_button(self):
        self.window.app_paths.remove(self.path)  # remove path from app_paths
        remove_path(self.path)
        self.window.buttons.remove(self)  # remove this button from buttons list
        self.window.canvas.delete(self.button_id)  
        self.button.destroy() 
        self.window.update_button_positions()  # update positions

    def update_icon(self, image):
        self.button.image = image  # Update reference
        self.button.config(image=image)  # Update configuration

    def update_path(self, path):
        self.path = path
        self.button.config(command=self.open_app)