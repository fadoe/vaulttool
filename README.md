# vaulttool

`vaulttool` ist ein kleines CLI-Werkzeug zur Verwaltung mehrerer [Obsidian](https://obsidian.md/)-Vaults. Es erlaubt einfache Git-Operationen, das Öffnen von Vaults mit verschiedenen Editoren und die Sicherung per Commit.

> Dieses Programm befindet sich noch in der Entwicklung.

---

## Funktionen

- `update` – zieht aktuelle Änderungen via `git pull`
- `push` – pusht lokale Änderungen ins Remote-Repository
- `backup` – packt alle Änderungen in einen stash und erstellt einen Commit mit Zeitstempel
- `repair` – setzt `.obsidian/workspace.json` zurück (nützlich bei UI-Problemen)
- `open` – öffnet einen Vault mit einem beliebigen konfigurierten Editor (z. B. Obsidian, PhpStorm, VSCode)

---

## Konfiguration

Die Konfiguration wird in einer YAML-Datei erwartet unter einem der folgenden Pfade:

- `~/.local/config/vaulttool/config.yaml`
- `~/.config/vaulttool/config.yaml`

### Beispiel `config.yaml`

```yaml
vaults:
  Work: ~/Documents/Vaults/Work
  Personal: ~/Documents/Vaults/Personal

editors:
  obsidian: xdg-open
  phpstorm: phpstorm
  code: code
```

Es muss immer auf Groß- und Kleinschreibung bei den Vaults geachtet werden. Sonst kann das Vault mit Obisidan nicht
geöffnet werden.

## Verwendung

CLI-Aufruf

```shell
vaulttool [action] [vaultname] [editor]
action ist eine der folgenden: update, push, backup, repair, open

vaultname ist der in der Konfiguration definierte Name

editor ist optional bei open (Standard: obsidian)
```

Beispiele

```shell
vaulttool update work
vaulttool push personal
vaulttool backup personal
vaulttool open work phpstorm
vaulttool open work             # öffnet mit Obsidian
```

## Einrichtung
1. Repository klonen
```shell
git clone <repo-url> ~/projects/vaulttool
cd ~/projects/vaulttool
```

2. Virtuelle Umgebung erstellen

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # falls notwendig
```

3. Shell-Wrapper ausführbar machen

```shell
chmod +x vaulttool
```
4. Verknüpfung ins System einrichten
```shell
mkdir -p ~/.local/bin
ln -s ~/projects/vaulttool/vaulttool ~/.local/bin/vaulttool
```

Stelle sicher, dass ~/.local/bin in deinem $PATH ist.

## Test

```bash
vaulttool --help        # Zeigt Usage
vaulttool update test   # Führt git pull auf Test-Vault aus
```

## Aufgaben

- [x] alle konfigurierten Vaults auflisten
- [x] alle konfigurierten Programme auflisten

## Lizenz

MIT – Verwendung auf eigene Verantwortung.

## Hinweise

- Git muss installiert sein.
- Für das Öffnen mit xdg-open oder phpstorm müssen die Programme im $PATH verfügbar sein.
- Pfade mit ~ werden korrekt aufgelöst.
