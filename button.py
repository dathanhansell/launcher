import tkinter as tk
from tkinter import messagebox
from config import remove_path

class Button:
    def __init__(self, window, path, image, callback, labelString=None):
        self.window = window
        self.path = path
        self.callback = callback
        self.button = tk.Button(window.root, image=image, command=self.run_callback(),
                                bd=0, bg="#222222", activebackground="#222222")
        self.button.image = image
        self.button.config(image=image)
        self.button.bind("<Button-3>", self.confirm_removal)
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)
        self.labelString = labelString
        self.button_id = self.window.canvas.create_window(
            0, 0, window=self.button, anchor='center')
        if self.labelString is not None:
            self.label = tk.Label(window.root, text=self.labelString, bg="#222222", fg="white")
            self.label.place(in_=self.button, relx=0.5, rely=1, anchor='center')

    def run_callback(self):
        return lambda: self.callback(self.window, self.path)

    def confirm_removal(self, event):
        if messagebox.askokcancel("Remove Button", "Do you really want to delete this button?", parent=self.window.root):
            self.remove_button()
        return "break"

    def remove_button(self):
        self.window.app_paths.remove(self.path)
        remove_path(self.path)
        self.window.buttons.remove(self)
        self.window.canvas.delete(self.button_id)
        self.button.destroy()
        self.window.update_button_positions()

    def update_icon(self, image):
        self.button.image = image
        self.button.config(image=image)

    def update_path(self, path):
        self.path = path
        self.button.config(command=self.run_callback())

    def on_enter(self, event):
        if self.window.enable_hover_effect:
            self.window.canvas.move(self.button_id, 0, 2)

    def on_leave(self, event):
        if self.window.enable_hover_effect:
            self.window.canvas.move(self.button_id, 0, -2)
