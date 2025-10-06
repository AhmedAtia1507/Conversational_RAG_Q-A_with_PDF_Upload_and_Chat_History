import yaml
import os
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigReader(metaclass=Singleton):
    def __init__(self, config_file="config.yaml"):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", config_file))
        self.config_file = config_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)

    def get(self, key, default=None):
        if key not in self.config:
            print(f"Warning: {key} not found in config.")
        return self.config.get(key, default)
