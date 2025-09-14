import subprocess

from vault import Vault

class EditorNotFoundError(Exception):
    pass

class VaultTool:
    def __init__(self, config):
        self.vaults = {name: Vault(name, path) for name, path in config.vaults.items()}
        self.editors = config.editors

    def get_vault(self, name: str) -> Vault:
        if name not in self.vaults:
            raise KeyError(f"Vault '{name}' nicht gefunden.")
        return self.vaults[name]

    def list_vaults(self):
        for vault_name, vault in self.vaults.items():
            print(f"{vault_name} -> {vault.path}")

    def list_programs(self):
        for program, command in self.editors.items():
            print(f"{program}: {command}")

    def open_vault(self, vault_name: str, program: str):
        if program not in self.editors:
            raise EditorNotFoundError(f"Program '{program}' is not configured.")

        vault = self.get_vault(vault_name)
        cmd = self._build_open_command(program, vault)
        print(f"Open vault '{vault_name}' with '{program}' ...")
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _build_open_command(self, program: str, vault: Vault) -> list:
        if program == "finder":
            param = vault.path
        elif program == "obsidian":
            param = f"obsidian://open?vault={vault.name}"
        else:
            param = str(vault.path)
        return [self.editors[program], param]
