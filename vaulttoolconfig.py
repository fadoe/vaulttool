from pathlib import Path
import yaml

class ConfigNotFoundError(Exception):
    pass

class VaultToolConfig:
    def __init__(self, config_locations: list):
        config_path = self._find_config(config_locations)
        data = self._load(config_path)
        self._validate_config(data)
        self.data = data

    @staticmethod
    def _find_config(config_locations: list) -> Path:
        for path in config_locations:
            if path.exists():
                return path
        raise ConfigNotFoundError("Configuration not found.", config_locations)

    @staticmethod
    def _load(config_path: Path) -> dict:
        with config_path.open("r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def _validate_config(config: dict) -> None:
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary.")
        if "vaults" not in config or not isinstance(config["vaults"], dict):
            raise ValueError("Config must have a 'vaults' attribute of type dict.")
        if "editors" not in config or not isinstance(config["editors"], dict):
            raise ValueError("Config must have an 'editors' attribute of type dict.")
        for name, path in config["vaults"].items():
            if not isinstance(name, str) or not isinstance(path, str):
                raise ValueError("Vault names and paths must be strings.")
        for program, command in config["editors"].items():
            if not isinstance(program, str) or not isinstance(command, str):
                raise ValueError("Editor names and commands must be strings.")

    @property
    def vaults(self) -> dict:
        return self.data.get("vaults", {})

    @property
    def editors(self) -> dict:
        return self.data.get("editors", {})
