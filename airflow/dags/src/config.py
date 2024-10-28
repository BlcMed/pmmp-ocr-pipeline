import json
from pathlib import Path
from typing import Dict


def load_config(config_file="config.json") -> Dict:
    """
    Load configuration settings from a JSON file.

    Args:
        config_file (str): Path to the configuration file. Default is "config.json".

    Returns:
        Dict[str, any]: Configuration settings as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.Args:
        config_file (str): Path to the configuration file. Default is "config.json".

    """
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_file} not found.")

    with open(config_path, "r") as f:
        return json.load(f)
