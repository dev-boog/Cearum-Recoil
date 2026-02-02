import json
import os

class ConfigManager:
    CONFIG_FILE = "config.json"
    
    DEFAULT_CONFIG = {
        "enable": False,
        "toggle_keybind": "NONE",
        "require_aim": False,
        "loop_recoil": False,
        "randomisation": False,
        "return_crosshair": False,
        "randomisation_strength": 0.5,
        "recoil_scalar": 1.0,
        "x_control": 1.0,
        "y_control": 1.0,
        "scripts_dir": "./saved_scripts",
        "loaded_script": "NONE",
        "cycle_keybind": "NONE"
    }

    @staticmethod
    def load_config():
        if not os.path.exists(ConfigManager.CONFIG_FILE):
            return ConfigManager.DEFAULT_CONFIG.copy()
        
        try:
            with open(ConfigManager.CONFIG_FILE, "r") as f:
                config = json.load(f)
                # Merge with default to ensure all keys exist
                full_config = ConfigManager.DEFAULT_CONFIG.copy()
                full_config.update(config)
                return full_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return ConfigManager.DEFAULT_CONFIG.copy()

    @staticmethod
    def save_config(data):
        try:
            with open(ConfigManager.CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
