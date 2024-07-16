.ONESHELL:
.PHONY: setup venv install clean activate

ACTIVATE:=. venv/bin/activate

setup: venv install run
    
venv:
	@echo "Creating python virtual environment in 'venv' folder..."
	@python3 -m venv venv

install:
	@echo "Installing python packages..."
	@$(ACTIVATE)
	@pip install -r requirements.txt

clean:
	@echo "Cleaning previous python virtual environment..."
	@rm -rf venv

activate:
	@echo "Activating python virtual environment..."
	@$(ACTIVATE)

run:
	@echo "Running the application..."
	@$(ACTIVATE)
	@python3 main.py
