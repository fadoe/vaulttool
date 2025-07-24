#!/usr/bin/env bash
set -e

echo "Erstelle virtuelles Environment..."
python3 -m venv venv

echo "Installiere Abhängigkeiten..."
source venv/bin/activate
pip install --upgrade pip
pip install pyyaml

echo "Fertig! Du kannst 'make run' verwenden oder den Wrapper installieren."
