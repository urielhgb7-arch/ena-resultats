#!/bin/bash

# Security check script for ENA platform
# Runs pip-audit, Django deploy checks, and Bandit

echo "Running pip-audit on dependencies..."
pip-audit -r requirements.txt

echo -e "\nRunning Django deployment checks..."
python manage.py check --deploy

echo -e "\nRunning Bandit on the codebase..."
bandit -r apps/ config/
