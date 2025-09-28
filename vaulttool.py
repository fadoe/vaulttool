import subprocess
from typing import Dict

from vaulttoolconfig import VaultToolConfig
from vault import Vault


class EditorNotFoundError(Exception):
    pass


class VaultNotFoundError(Exception):
    pass


class VaultTool:
    def __init__(self, config: VaultToolConfig):
        self.vaults: Dict[str, Vault] = {name: Vault(name, path) for name, path in config.vaults.items()}
        self.programs: Dict[str, str] = config.programs

    def get_vault(self, name: str) -> Vault:
        if name not in self.vaults:
            raise VaultNotFoundError(f"Vault '{name}' not found.")
        return self.vaults[name]

    def list_vaults(self) -> dict[str, str]:
        return dict((name, str(vault.path)) for name, vault in self.vaults.items())

    def list_programs(self) -> dict[str, str]:
        return dict(self.programs.items())

    def open_vault(self, vault_name: str, program: str) -> None:
        if program not in self.programs:
            raise EditorNotFoundError(f"Program '{program}' is not configured.")

        vault = self.get_vault(vault_name)
        cmd = self._build_open_command(program, vault)
        print(f"Open vault '{vault_name}' with '{program}' ...")
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _build_open_command(self, program: str, vault: Vault) -> list[str]:
        if program == "finder":
            param = str(vault.path)
        elif program == "obsidian":
            param = f"obsidian://open?vault={vault.name}"
        else:
            param = str(vault.path)
        return [self.programs[program], param]
