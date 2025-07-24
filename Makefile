.PHONY: install run clean

install:
	bash install.sh

run:
	source venv/bin/activate && python vaulttool.py

clean:
	rm -rf venv

install-wrapper:
	mkdir -p ~/.local/bin
	ln -sf $(PWD)/vaulttool ~/.local/bin/vaulttool
