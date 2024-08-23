import json
from pathlib import Path

def load_config(config_file='config.json'):
    """
    Load configuration settings from a JSON file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: Configuration settings.
    """
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_file} not found.")
    
    with open(config_path, 'r') as f:
        return json.load(f)
