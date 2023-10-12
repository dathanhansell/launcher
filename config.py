import json,os

CONFIG_FILE = "config.json"

def load_paths():
    paths = []
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as file:
            pass
    
    with open(CONFIG_FILE, 'r') as file:
        if os.stat(CONFIG_FILE).st_size != 0:
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
