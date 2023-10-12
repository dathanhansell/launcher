import keyboard
from window import Window 

radial_window = Window()

keyboard.add_hotkey('ctrl + space', radial_window.toggle_visibility)

radial_window.root.mainloop()
