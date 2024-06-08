import win32com.client
import tempfile
import math
from icoextract import IconExtractor
from PIL import ImageTk, Image
import os
import sys
from tkinter import PhotoImage
import re

def button_layout(n):
    if n == 1:
        yield (0.5, 0.5)
    else:
        for i in range(n):
            yield (0.5-0.4*math.sin(2 * math.pi / n * i), 0.5-0.4*math.cos(2 * math.pi / n * i))

def parse_paths(input_string):
    path_pattern = re.compile(r'\{.*?\}|\S+')
    matches = path_pattern.findall(input_string)
    paths = [match.strip('{}') for match in matches]
    return paths

def clean_path(path):
    path = path.replace("{", "").replace("}", "")
    path = os.path.normpath(path)
    shell = win32com.client.Dispatch("WScript.Shell")
    if path.endswith('.lnk'):
        shortcut = shell.CreateShortCut(path)
        path = shortcut.Targetpath
    return path

def executable_path(path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    elif __file__:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, path)

def folder_icon():
    icon_path = executable_path('folder.png')

    if os.path.exists(icon_path):
        return PhotoImage(file=icon_path)
    else:
        raise FileNotFoundError(f"Folder icon not found at {icon_path}")


def extract_icon(path):
    try:
        path = clean_path(path)
        filename = os.path.splitext(os.path.basename(path))[0]
        cache_dir = ".cache"
        cache_file = os.path.join(cache_dir, filename) + ".ico"
        os.makedirs(cache_dir, exist_ok=True)

        if os.path.exists(cache_file):
            icon = Image.open(cache_file)
        else:
            try:
                with tempfile.NamedTemporaryFile(suffix=".ico", delete=False) as temp:
                    extractor = IconExtractor(path)
                    extractor.export_icon(temp.name)

                icon = Image.open(temp.name)
                icon.thumbnail((64, 64))
                icon.save(cache_file)
                icon.close()
                icon = Image.open(cache_file)
            finally:
                try:
                    os.unlink(temp.name)
                except PermissionError:
                    print("Unable to delete temp file {}, consider deleting it manually".format(
                        temp.name))
        return ImageTk.PhotoImage(icon)
    except Exception as e:
        print(f"Couldn't extract icon from path {path}, reason: {str(e)}")
