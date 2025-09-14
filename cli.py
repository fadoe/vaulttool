import sys
from config import Config, ConfigNotFoundError
from pathlib import Path
from vaulttool import VaultTool, EditorNotFoundError

CONFIG_LOCATIONS = [
    Path.home() / ".local/config/vaulttool/config.yaml",
    Path.home() / ".config/vaulttool/config.yaml"
]

def main():
    if len(sys.argv) < 2:
        print("Usage: vaulttool [update|push|repair|backup|open|list-vaults|list-programs] [vault-name] [program (optional)]", file=sys.stderr)
        sys.exit(1)

    action = sys.argv[1]

    try:
        config = Config(CONFIG_LOCATIONS)
    except ConfigNotFoundError:
        print("Configuration file not found.", file=sys.stderr)
        for p in CONFIG_LOCATIONS:
            print(f"  {p}", file=sys.stderr)
        sys.exit(1)

    tool = VaultTool(config)

    pre_actions = {
        "list-vaults": tool.list_vaults,
        "list-programs": tool.list_programs,
    }

    if action in pre_actions:
        pre_actions[action]()
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Vault name is missing.", file=sys.stderr)
        sys.exit(1)

    vault_name = sys.argv[2]
    editor = sys.argv[3] if len(sys.argv) > 3 else "obsidian"

    try:
        vault = tool.get_vault(vault_name)
    except KeyError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    actions = {
        "update": vault.update,
        "push": vault.push,
        "repair": vault.repair,
        "backup": vault.backup,
        "open": lambda: tool.open_vault(vault_name, editor),
    }

    if action not in actions:
        print(f"Unknown action '{action}'.", file=sys.stderr)
        sys.exit(1)

    try:
        actions[action]()
    except EditorNotFoundError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
