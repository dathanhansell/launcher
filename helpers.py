import math
from icoextract import IconExtractor
from PIL import ImageTk, Image
import os

def button_layout(n):
    if n == 1:
        yield (0.5, 0.5) 
    else:
        for i in range(n):
            yield (0.5-0.4*math.sin(2 * math.pi / n * i), 0.5-0.4*math.cos(2 * math.pi / n * i))

from icoextract import IconExtractor

import tempfile
import win32com.client
def clean_path(path):

    
        path = path.replace("{", "").replace("}", "")
        path = os.path.normpath(path)
        shell = win32com.client.Dispatch("WScript.Shell")
        if path.endswith('.lnk'):
            shortcut = shell.CreateShortCut(path)
            path = shortcut.Targetpath 
        return path

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
                    print("Unable to delete temp file {}, consider deleting it manually".format(temp.name))
        return ImageTk.PhotoImage(icon)
    except Exception as e:
        print(f"Couldn't extract icon from path {path}, reason: {str(e)}")
