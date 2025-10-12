import yaml
import os
class Singleton(type):
    """
    A metaclass that implements the Singleton design pattern.

    This metaclass ensures that only one instance of a class can be created.
    When a class uses this metaclass, subsequent attempts to instantiate the class
    will return the same instance that was created on the first instantiation.

    Attributes:
        _instances (dict): A class-level dictionary that stores the single instance
                          of each class that uses this metaclass, keyed by the class type.

    Methods:
        __call__(*args, **kwargs): Overrides the default instance creation behavior
                                   to ensure singleton pattern is maintained.

    Usage:
        class MyClass(metaclass=Singleton):
            pass
        
        # Both variables will reference the same instance
        obj1 = MyClass()
        obj2 = MyClass()
        assert obj1 is obj2  # True

    Note:
        This implementation is not thread-safe. In multi-threaded environments,
        additional synchronization mechanisms should be considered.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigReader(metaclass=Singleton):
    """
    A singleton configuration reader class for loading and accessing YAML configuration files.
    This class implements the Singleton pattern to ensure only one instance of the configuration
    reader exists throughout the application lifecycle. It loads configuration from a YAML file
    and provides methods to access configuration values.
    Attributes:
        config_file (str): Absolute path to the configuration file.
        config (dict): Loaded configuration data from the YAML file.
    Methods:
        load_config(): Loads the YAML configuration file and returns its contents.
        get(key, default=None): Retrieves a configuration value by key with optional default.
    Example:
        >>> config_reader = ConfigReader("my_config.yaml")
        >>> database_url = config_reader.get("database_url", "localhost")
        >>> api_key = config_reader.get("api_key")
    Note:
        This class uses the Singleton metaclass, so multiple instantiations will return
        the same instance. The configuration file path is resolved relative to the
        parent directory of the current file.
    """
    def __init__(self, config_file="config.yaml"):
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", config_file))
        self.config_file = config_path
        self.config = self.load_config()

    def load_config(self):
        """
        Load configuration data from a YAML file.
        
        Opens and reads the YAML configuration file specified by self.config_file,
        then parses it into a Python dictionary using safe loading to prevent
        execution of arbitrary code.
        
        Returns:
            dict: A dictionary containing the configuration data loaded from the YAML file.
            
        Raises:
            FileNotFoundError: If the configuration file specified by self.config_file 
                              does not exist.
            yaml.YAMLError: If the YAML file contains invalid syntax or cannot be parsed.
            PermissionError: If there are insufficient permissions to read the file.
        """
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)

    def get(self, key, default=None):
        """
        Retrieve a configuration value by key with optional default fallback.

        Args:
            key (str): The configuration key to retrieve.
            default (optional): The default value to return if the key is not found.
                               Defaults to None.

        Returns:
            The value associated with the key if found, otherwise the default value.

        Note:
            Prints a warning message if the requested key is not found in the configuration.
        """
        if key not in self.config:
            print(f"Warning: {key} not found in config.")
        return self.config.get(key, default)
