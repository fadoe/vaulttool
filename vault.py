import subprocess
from datetime import datetime
from pathlib import Path

class Vault:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = Path(path).expanduser()

    def run_git(self, args: list):
        subprocess.run(["git", "-C", str(self.path)] + args, check=True)

    def update(self):
        self.run_git(['pull', '--rebase', '--autostash'])

    def push(self):
        self.run_git(['push'])

    def repair(self):
        self.run_git(['restore', '--staged', '.obsidian/workspace.json'])

    def backup(self):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"vault backup: {ts}"
        self.run_git(['add', '--all'])
        self.run_git(['commit', '-m', msg])
