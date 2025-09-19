import subprocess
from typing import Dict, Any

from vault import Vault


class EditorNotFoundError(Exception):
    pass


class VaultTool:
    def __init__(self, config: Any):
        self._validate_config(config)
        self.vaults: Dict[str, Vault] = {name: Vault(name, path) for name, path in config.vaults.items()}
        self.editors: Dict[str, str] = config.editors

    def get_vault(self, name: str) -> Vault:
        if name not in self.vaults:
            raise KeyError(f"Vault '{name}' not found.")
        return self.vaults[name]

    def list_vaults(self) -> None:
        for vault_name, vault in self.vaults.items():
            print(f"{vault_name} -> {vault.path}")

    def list_programs(self) -> None:
        for program, command in self.editors.items():
            print(f"{program}: {command}")

    def open_vault(self, vault_name: str, program: str) -> None:
        if program not in self.editors:
            raise EditorNotFoundError(f"Program '{program}' is not configured.")

        vault = self.get_vault(vault_name)
        cmd = self._build_open_command(program, vault)
        print(f"Open vault '{vault_name}' with '{program}' ...")
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    def _validate_config(config: Any) -> None:
        if not hasattr(config, 'vaults') or not isinstance(config.vaults, dict):
            raise ValueError("Config must have a 'vaults' attribute of type dict.")
        if not hasattr(config, 'editors') or not isinstance(config.editors, dict):
            raise ValueError("Config must have an 'editors' attribute of type dict.")
        for name, path in config.vaults.items():
            if not isinstance(name, str) or not isinstance(path, str):
                raise ValueError("Vault names and paths must be strings.")
        for program, command in config.editors.items():
            if not isinstance(program, str) or not isinstance(command, str):
                raise ValueError("Editor names and commands must be strings.")

    def _build_open_command(self, program: str, vault: Vault) -> list[str]:
        if program == "finder":
            param = str(vault.path)
        elif program == "obsidian":
            param = f"obsidian://open?vault={vault.name}"
        else:
            param = str(vault.path)
        return [self.editors[program], param]
