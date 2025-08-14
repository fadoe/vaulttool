#!/usr/bin/env python3
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import yaml

CONFIG_LOCATIONS = [
    Path.home() / ".local/config/vaulttool/config.yaml",
    Path.home() / ".config/vaulttool/config.yaml"
]

def find_config_file():
    for path in CONFIG_LOCATIONS:
        if path.exists():
            return path
    return None

def load_config():
    config_path = find_config_file()
    if not config_path:
        print("❌ Konfigurationsdatei nicht gefunden.", file=sys.stderr)
        print("Erwartete Pfade:", file=sys.stderr)
        for path in CONFIG_LOCATIONS:
            print(f"  {path}", file=sys.stderr)
        sys.exit(1)
    with config_path.open("r") as f:
        return yaml.safe_load(f)

def run_git_command(path: Path, args: list):
    subprocess.run(["git", "-C", str(path)] + args, check=True)

def build_open_with_program_command(program: str, command: str, vault_name: str, vault_path: Path) -> list:
    if program == "finder":
        param = vault_path
    elif program == "obsidian":
        param = f"obsidian://open?vault={vault_name}"
    else:
        param = str(vault_path)
    return [command, param]

def do_update(vault_path: Path):
    run_git_command(vault_path, ['pull', '--rebase', '--autostash'])

def do_push(vault_path: Path):
    run_git_command(vault_path, ['push'])

def do_repair(vault_path: Path):
    run_git_command(vault_path, ['restore', '--staged', '.obsidian/workspace.json'])

def do_backup(vault_path: Path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"vault backup: {timestamp}"
    run_git_command(vault_path, ['add', '--all'])
    run_git_command(vault_path, ['commit', '-m', commit_msg])

def do_open(vault_name: str, vault_path: Path, editor: str, editors: dict):
    if editor not in editors:
        print(f"Editor '{editor}' nicht in der Konfiguration.", file=sys.stderr)
        sys.exit(1)
    cmd = build_open_with_program_command(editor, editors[editor], vault_name, vault_path)
    print(f"Öffne Vault '{vault_name}' mit '{editors[editor]}' ...")
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    if len(sys.argv) < 3:
        print("Usage: vaulttool.py [update|push|repair|backup|open] [vaultname] [editor (optional)]", file=sys.stderr)
        sys.exit(1)

    action, vault_name = sys.argv[1], sys.argv[2]
    chosen_editor = sys.argv[3] if len(sys.argv) > 3 else "obsidian"

    config = load_config()
    vaults = config.get("vaults", {})
    editors = config.get("editors", {})

    if vault_name not in vaults:
        print(f"❌ Vault '{vault_name}' nicht gefunden.", file=sys.stderr)
        sys.exit(1)

    vault_path = Path(vaults[vault_name]).expanduser()

    actions = {
        "update": lambda: do_update(vault_path),
        "push": lambda: do_push(vault_path),
        "repair": lambda: do_repair(vault_path),
        "backup": lambda: do_backup(vault_path),
        "open": lambda: do_open(vault_name, vault_path, chosen_editor, editors),
    }

    if action not in actions:
        print(f"❌ Unbekannte Aktion '{action}'.", file=sys.stderr)
        sys.exit(1)

    actions[action]()

if __name__ == "__main__":
    main()
