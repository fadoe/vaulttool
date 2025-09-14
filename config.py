from pathlib import Path
import yaml

class ConfigNotFoundError(Exception):
    pass

class Config:
    def __init__(self, config_locations: list):
        self.config_path = self._find_config(config_locations)
        self.data = self._load()

    @staticmethod
    def _find_config(config_locations: list) -> Path:
        for path in config_locations:
            if path.exists():
                return path
        raise ConfigNotFoundError("Configuration not found.")

    def _load(self) -> dict:
        with self.config_path.open("r") as f:
            return yaml.safe_load(f)

    @property
    def vaults(self) -> dict:
        return self.data.get("vaults", {})

    @property
    def editors(self) -> dict:
        return self.data.get("editors", {})
