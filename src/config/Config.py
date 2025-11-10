import yaml
from pathlib import Path
from typing import Dict, List, Any


class ConfigError(Exception):
    """Custom exception for invalid config format."""
    pass


class Config:
    def __init__(self):
        self.source_city_map: Dict[str, List[str]] = {}
        self.polling_time: int = 0
        self._load()

    def _load(self):
        try:
            with open("config/config.yaml", "r") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError as e:
            raise ConfigError(f"No config file found: {e}")

        # Validate top-level keys
        if not isinstance(data, dict):
            raise ConfigError("Config must be a JSON object")
        if "source_city_map" not in data or "polling_time" not in data:
            raise ConfigError("Config must contain 'source_city_map' and 'polling_time' keys")

        # Validate source_city_map
        scm = data["source_city_map"]
        if not isinstance(scm, dict):
            raise ConfigError("'source_city_map' must be a dictionary")
        for key, value in scm.items():
            if not isinstance(key, str):
                raise ConfigError(f"Source name must be a string, got {key}")
            if not isinstance(value, list) or not all(isinstance(city, str) for city in value):
                raise ConfigError(f"Cities for source '{key}' must be a list of strings")

        self.source_city_map = scm

        # Validate polling_time
        pt = data["polling_time"]
        if not isinstance(pt, int) or pt <= 0:
            raise ConfigError("'polling_time' must be a positive integer")
        self.polling_time = pt