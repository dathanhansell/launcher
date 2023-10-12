import json,os

CONFIG_FILE = "config.json"

def load_paths():
    paths = []
    with open('config.json', 'r') as file:
        if os.stat('config.json').st_size != 0:  # check if file is not empty
            paths = json.load(file)
    return paths
        
def save_path(path):
    paths = load_paths()
    paths.append(path)
    with open(CONFIG_FILE, "w") as file:
        json.dump(paths, file)
def remove_path(target_path):
    paths = load_paths()
    if target_path in paths:
        paths.remove(target_path)
        with open(CONFIG_FILE, "w") as file:
            json.dump(paths, file)
