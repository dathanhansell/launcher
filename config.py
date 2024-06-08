import json
import os

CONFIG_FILE = "config.json"

def load_paths():
    config = load_config()
    return config.get("paths", [])

def save_path(path):
    config = load_config()
    paths = config.get("paths", [])
    if path not in paths and len(path) > 0:
        print(path, " added to paths")
        paths.append(path)
        config["paths"] = paths
        save_config(config)
        return path

def path_exists(path):
    paths = load_paths()
    print("pathin in paths:", path in paths)
    return path in paths

def remove_path(path):
    config = load_config()
    paths = config.get("paths", [])
    if path in paths:
        paths.remove(path)
        print(path, " removed from paths")
        config["paths"] = paths
        save_config(config)

def load_config():
    default_config = {
        "paths": [],
        "show_labels_on_programs": False,
        "show_labels_on_directories": True,
        "hide_launcher_on_icon_click": True,
        "radius": 400,
        "enable_hover_effect": True
    }
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            if os.stat(CONFIG_FILE).st_size != 0:
                user_config = json.load(file)
                if isinstance(user_config, list):
                    user_config = {"paths": user_config}  # Convert old format to new format
                default_config.update(user_config)
    return default_config

def save_config(config):
    config_to_save = load_config()
    for key, value in config.items():
        if key != "paths" or (key == "paths" and value):  # Only update paths if it's not empty
            config_to_save[key] = value
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_to_save, file)
